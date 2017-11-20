#!/bin/perl

#INPUT
#Input order: director folder_prefix .gro, .top, z_low, z_up, Bin_num, is_write
#like : perl bash_MoS2.sh /home/lz/lz/Simulation/MoS2/build/1T-MoS2/ 1T_MoS2_ gro top 0 20 2000 -1_1_1
#python: python WritePara.py -i end.gro -p end.top -w "-1 1 1" -l 0 -u 40 -n 2000

$Dir_code=`pwd`;
chomp($Dir_code);

sub GetFolder{                                                                                                              my @temp;                                                                                                                   if($_[0]){                       
    chdir $_[0];
    @folder=<{$_[1]*/}>;                                                                                                      foreach $folder(@folder){                                                                                                   @temp = (@temp,"$_[0]$folder");                             
    }
    chdir $Dir_code;
}
    return @temp;
}

@folder=GetFolder($ARGV[0],$ARGV[1]);

foreach $folder(@folder){
  system "cp WritePara.py $folder";
  chdir $folder;
  system "python WritePara.py -i $ARGV[2] -p $ARGV[3] -l $ARGV[4] -u $ARGV[5] -n $ARGV[6] -w $ARGV[7]";
  system "rm -f WritePara.py";
  chdir $Dir_code;
}


#for($i=0;$i<$TDir;$i+=1){
#  system "cp *.sh *.py *.pl *.mdp @Prex[$i]";
#  chdir @Prex[$i];
#  system "perl main.pl @Gro[$i] @Top[$i] $DetaBin $BulkDens $Delete";                  
#  system "rm -f bash.sh bash_multi.sh *.py *.sh *.pl STANDARD_EM.mdp STANDARD_NVT.mdp em.mdp initial.mdp tune.mdp";  
#  chdir $Dir_code;
#}
