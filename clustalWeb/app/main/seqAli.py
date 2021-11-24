import os
from glob import glob
from Bio.Align.Applications import ClustalwCommandline
from Bio import AlignIO, SeqIO 
from .fastaOp import saveFasta

clustal_loc = r"/home/glbf/clustalw-2.1/src/clustalw2"

def is_fasta(filename): 
    with open(filename, "r") as handle: 
     fasta = SeqIO.parse(handle, "fasta") 
     return any(fasta) # False when `fasta` is empty, i.e. wasn't a FASTA file 


def clu(workTime):
    assert os.path.isfile(clustal_loc), "Clustal W not found"
    basepath = os.path.dirname(__file__)
    fastaPath = os.path.join(basepath, "history/" + "Sequences" + workTime + ".fasta") 
    assert is_fasta(fastaPath) , "your input is not fasta"
    try:
        alnPath = os.path.join(basepath, "./output/" + "Aligned" + workTime + ".aln") 
        print(fastaPath)
        clustalw_cline = ClustalwCommandline(
            clustal_loc, infile=fastaPath, outfile=alnPath)
        print(clustalw_cline)
        stdout, stderr = clustalw_cline()
        align = AlignIO.read(alnPath, "clustal")
        return align
    except Exception:
        print("There was a problem aligning. Check ClustalW path and .fasta folder format/location")


if __name__ == '__main__':
    seq1 = {"test1": "ATCGCTAGATCGCTAGTTCCGGATCGCTAA"}
    seq2 = {"test2": "ATCGCTAGTTCCGTAGTTCGCTAG"}
    import time
    workTime = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
    saveFasta(workTime,seq1, seq2)
    b=clu(workTime)
    for a in b:
        print(a)
