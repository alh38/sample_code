#!/usr/bin/env python3
import subprocess
import pandas as pd
import os

def run(cmd):
   proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
   proc.communicate()
   
def run_merqury(assembly,R1,R2):
    # check that assembly fasta and fastqs exist and aren't empty, and if so, make local copies; this is probably the most important step since merqury can behave strangely with missing/empty input and with absolute paths
    if assembly.is_file():
        cmd = 'cp ' + assembly + ' assembly.fasta'
        run(cmd)   
    else
        print('%s does not exist.' % assembly)
        sys.exit(1)
    empty_bool = os.stat('assembly.fasta').st_size == 0
    if empty_bool is True:
        print('%s is empty.' % assembly)
        sys.exit(1)
    if R1.is_file() and R2.is_file():
        if R1.endswith('.gz'):
            cmd = 'cp ' + R1 + ' R1.fq.gz'
            run(cmd)
            cmd = 'cp ' + R2 + ' R2.fq.gz'
            run(cmd)
            cmd = 'gunzip R*.fq.gz'
            run(cmd)
            cmd = 'cat R*.fq > reads.fq'
            run(cmd)
            empty_bool = os.stat('reads.fq').st_size == 0
            if empty_bool is True:
                print('Fastqs are empty.')
                sys.exit(1)
        else:
            cmd = 'cat ' + R1 + ' ' + R2 + ' > reads.fq'
            run(cmd)
            empty_bool = os.stat('reads.fq').st_size == 0
            if empty_bool is True:
                print('Fastqs are empty.')
                sys.exit(1)
    # run meryl to count 31-mers in reads
    cmd = 'meryl count k=31 reads.fq output read_31mers.meryl'
    run(cmd)
    # run merqury to calculate assembly qv/error rate
    cmd = '$MERQURY/merqury.sh read_31mers.meryl assembly.fasta assembly_merqury'
    run(cmd)
