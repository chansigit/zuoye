# -*- coding: utf-8 -*-
"""
Created on 8th Mar

@author: CyLiu
"""

from StepBase import Step, Configure
import subprocess
import os

class TrimPolyA(Step):
    def __init__(self,
                 bamInput = None,
                 bamOutputDir = None,
                 sumOutputDir = None,
                 misMatches = 0,
                 numBases = 5,
                 cmdParam = None,
                 **kwargs):
        super(Step, self).__init__(cmdParam, **kwargs)

        self.setParamIO('bamInput', bamInput)
        self.setParamIO('bamOutputDir', bamOutputDir)
        self.setParamIO('sumOutputDir', sumOutputDir)

        self.initIO()

        self.setParam('misMatches', misMatches)
        self.setParam('numBases', numBases)

    def impInitIO(self,):
        bamInput = self.getParamIO('bamInput')
        bamOutputDir = self.getParamIO('bamOutputDir')
        sumOutputDir = self.getParamIO('sumOutputDir')

        self.setInputDirOrFile('bamInput', bamInput)
        self.setOutputDirNTo1('bamOutput', os.path.join(bamOutputDir, 'unaligned_mc_tagged_polyA_filtered.bam'), '', 'bamInput')
        self.setOutputDirNTo1('sumOutput', os.path.join(sumOutputDir, 'polyA_trimming_report.txt'), '', 'bamInput')

        if bamInput is not None:
            self._setInputSize(len(self.getInputList('bamInput')))

    def call(self, *args):
        bamUpstream = args[0]
        self.setParamIO('bamInput', bamUpstream.getOutput('bamOutput'))

    def _singleRun(self, i):
        bamInput = self.getInputList('bamInput')
        bamOutput = self.getOutputList('bamOutput')
        sumOutput = self.getOutputList('sumOutput')

        misMatches = self.getParam('misMatches')
        numBases = self.getParam('numBases')

        cmdline = [
                '../../dropseq/Drop-seq_tools-1.13/PolyATrimmer',
                'INPUT=%s'%(bamInput[i]), 'OUTPUT=%s'%(bamOutput[i]),
                'OUTPUT_SUMMARY=%s'%(sumOutput[i]),
                'MISMATCHES=%d'%(misMatches), 'NUM_BASES=%d'%(numBases)
        ]
        self.callCmdline(cmdline)
