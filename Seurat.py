# -*- coding: utf-8 -*-
"""
@author: Zhenyi Wang
"""

from StepBase import Step,Configure
import subprocess
import os

class Seurat(Step):
    def __init__(self,
                 Matrixdata = None,                 
                 barcodes = None, 
                 genes = None,
                 outputDir = None,
                 threads = None,
                 cmdParam = None, 
                 **kwargs):
        super(Step, self).__init__(cmdParam,**kwargs)
        """
        __init__(): Initialize the class with inputs, outputs and other parameters.
        Setting all parameter is the main target of this function.
        """
        
        # set all input and output parameters
        self.setParamIO('Matrixdata',Matrixdata)
        self.setParamIO('barcodes',barcodes)   
        self.setParamIO('genes',genes) 
        self.setParamIO('outputDir',outputDir) 
        # call self.initIO()
        self.initIO()
        #set other parameters
        if threads is None:
            threads = Configure.getThreads()
        self.setParam('threads',threads)
        self._setMultiRun()
        
    def impInitIO(self,):
        """
        This function is to initialize 
        all of the input and output files from the io parameters set in __init__() 
        """
        # obtain all input and output parameters        
        Matrixdata = self.getParamIO('Matrixdata')
        barcodes = self.getParamIO('barcodes')   
        genes = self.getParamIO('genes')  
        outputDir = self.getParamIO('outputDir')  
        
        #set all input files        
        self.setInputDirOrFile('Matrixdata', Matrixdata)
        self.setInputDirOrFile('barcodes', barcodes)
        self.setInputDirOrFile('genes', genes)

        # create output file paths and set
        self.setOutputDir1To1('VlnPlot', outputDir,'VlnPlot','jpg','genes') 
        self.setOutputDir1To1('GenePlot', outputDir,'GenePlot','jpg','genes')
        if outputDir is None:
            self.setParamIO('outputDir',Configure.getTmpDir())     

    def call(self, *args):
        """
        called by Seurat()(object)
        """
        # the first object
        cellrangerUpstream = args[0]      
        
        # set all required input parameters from upstream object
        self.setParamIO('Matrixdata',cellrangerUpstream.getParamIO('outputDir'))
        

    def _multiRun(self,):
        Matrixdata = self.getInput('Matrixdata')
        barcodes = self.getInput('barcodes')
        genes = self.getInput('genes')
        VlnPlot = self.getOutput('VlnPlot')
        GenePlot = self.getOutput('GenePlot')
        cmdline = ['Rscript',
        		   'Seurat.R',
        			Matrixdata,
                    barcodes,
                    genes,
                    self.getParamIO('outputDir')
        			]
        # cmdline = ' '.join(cmdline)		     
        print(' '.join(cmdline))      
        self.callCmdline(cmdline)
           
            