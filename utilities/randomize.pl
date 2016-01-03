#!/usr/bin/perl

#undef $/;

use strict;
use warnings;
use JSON;


my @array;
open(my $fh, "<", "users_havinggists.json")
    or die "Failed to open file: $!\n";
while(<$fh>) { 
    chomp; 
    push @array, $_;
} 
close $fh;

my @decoded_json = @{decode_json(@array)};

fisher_yates_shuffle(\@decoded_json);

open $fh, ">", "users_havinggists.json";
print $fh encode_json(\@decoded_json);
close $fh;

exit;


# fisher_yates_shuffle( \@array ) : generate a random permutation
# of @array in place
sub fisher_yates_shuffle {
    my $array = shift;
    my $i;
    for ($i = @$array; --$i; ) {
        my $j = int rand ($i+1);
        next if $i == $j;
        @$array[$i,$j] = @$array[$j,$i];
    }
}

