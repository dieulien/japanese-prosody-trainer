#!/usr/bin/perl
#
# perform forced alignment using Julius-4
#
# usage: segment_julius4.pl speechfile transfile
#
# output will be written to 'trans.align', and
# Julius log will be stored in 'trans.log'
#

######################################################################
######################################################################
#### user configuration

## julius4 executable
$julius4bin="/usr/local/bin/julius";

## acoustic model
$basedir="/cdrom/IPA_0103";
$hmmdefs="$basedir/phone_m/model/monof/mix16/gid/hmmdefs.gz";

## HMMList file (needed if above is triphone based model)
#$hlist="$basedir/phone_m/parms/logicalTri.added";

## working directory
$TMPDIR=".";

## other options to Julius4
$OPTARGS="-input file";	# raw speech file input
#$OPTARGS="-input htkparam";	# MFCC file input

## enable debug message
$debug_flag=0;			# set to 1 for debug output to speechfile.log

######################################################################
######################################################################

#### initialize
if ($#ARGV < 1) {
    print "usage: segment_julius4.pl speech_file trans_file\n";
    exit;
}
$speechfile = $ARGV[0];
$transfile  = $ARGV[1];
if (! -r $speechfile) {
    die "Error: cannot open speech file \"$speechfile\"\n";
}
if (! -r $transfile) {
    die "Error: cannot open trans. file \"$transfile\"\n";
}

#### open result file for writing
$logfile = $transfile . ".align";
open(RESULT, ">$logfile") || die "Error: cannot open result file \"$logfile\"\n";

#### generate speech grammar 'tmp.dfa' and 'tmp.dict' from transcription

# clean temporary file
unlink("$TMPDIR/tmp.dfa") if (-r "$TMPDIR/tmp.dfa");
unlink("$TMPDIR/tmp.dict") if (-r "$TMPDIR/tmp.dict");

## read transcription
print RESULT "--- transcription ---\n";
@words=();
open(TRANS, "$transfile") || die "Error: cannot open speech file \"$transfile\"\n";
while(<TRANS>) {
    chomp;
    next if /^[ \t\n]*$/;
    push(words, $_);
    print RESULT "$_\n";
}
close(TRANS);
$num = $#words;

# write dfa
print RESULT "--- generated DFA ---\n";
open(DFA, ">$TMPDIR/tmp.dfa") || die "Error: cannot open $TMPDIR/tmp.dfa for writing\n";
for ($i = 0; $i <= $num; $i++) {
    $str = sprintf("%d %d %d 0", $i, $num - $i, $i + 1);
    if ($i == 0) {
	$str .= " 1\n";
    } else {
	$str .= " 0\n";
    }
    print DFA "$str";
    print RESULT "$str";
}
$str = sprintf("%d -1 -1 1 0\n", $num + 1);
print DFA "$str";
print RESULT "$str";
close(DFA);

# write dict
print RESULT "--- generated dict ---\n";
open(DICT, ">$TMPDIR/tmp.dict") || die "Error: cannot open $TMPDIR/tmp.dict for writing\n";
for ($i = 0; $i <= $num; $i++) {
    $w = shift(@words);
    $str = "$i [w_$i] $w\n";
    $WLIST{"w_$i"} = "$w";
    print DICT "$str";
    print RESULT "$str";
}
### (ri) quick hack to avoid error in Julius 3.4 and 3.4.1...
#if ($num == 0) {
#    $str = "$num [w_$num] $w\n";
#    print DICT "$str";
#    print RESULT "$str";
#}
###
close(DICT);

print RESULT "----------------------\n\n";

# check generated files
if ((! -r "$TMPDIR/tmp.dfa") || (! -f "$TMPDIR/tmp.dfa")) {
    die "Error: failed to make \"$TMPDIR/tmp.dfa\"\n";
}
if ((! -r "$TMPDIR/tmp.dict") || (! -f "$TMPDIR/tmp.dict")) {
    die "Error: failed to make \"$TMPDIR/tmp.dict\"\n";
}

#### execute Julius4 and store the output to log
#$command = "echo $speechfile | $julius4bin -h $hmmdefs -dfa $TMPDIR/tmp.dfa -v $TMPDIR/tmp.dict -palign";
$command = "echo $speechfile | $julius4bin -h $hmmdefs -dfa $TMPDIR/tmp.dfa -v $TMPDIR/tmp.dict";
if ($num > 0) {		# more than 1 line in trans
    $command .= " -walign";
}else{
    $command .= " -palign";
}
if ($hlist ne "") {
    $command .= " -hlist $hlist";
}
$command .= " $OPTARGS";
$command .= " -debug" if ($debug_flag != 0);

system("$command > ${transfile}.log");

#### remove temporary file
unlink("$TMPDIR/tmp.dfa");
unlink("$TMPDIR/tmp.dict");

#### parse log and append result to speechfile.align
open(LOG, "${transfile}.log") || die "Error: cannot open julius4 log file\n";
print RESULT "============ ALIGNMENT RESULT ============\n";
$sw = 0;
while(<LOG>) {
    chomp;
    if (/^Stat:\s+adin_file:/) {
	s/^Stat:\s+adin_file:\s+//;
	print RESULT "$_\n";
	next;
    }
    if (/^STAT:\s+\d+\s+samples/) {
	s/^STAT:\s+//;
	print RESULT "$_\n";
	next;
    }
    if (/^=== begin forced alignment ===$/) {
	$sw = 1;
    }
    if ($sw == 1) {
	if(/\[(w_\d+)\]/){
	    $c_str = $1;
	    s/$c_str/$WLIST{$c_str}/;
	}
	print RESULT "$_\n";
    }
    if (/^=== end forced alignment ===$/) {
	$sw = 0;
    }
}
close(LOG);
close(RESULT);

#### end of processing
print "Log saved in \"${transfile}.log\"\n";
print "Result saved in \"$logfile\".\n";
