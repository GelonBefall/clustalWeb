import os

# Create Fasta file
def saveFasta(workTime,*data):
    basepath = os.path.dirname(__file__)
    fastaPath = os.path.join(basepath, "history/" + "Sequences" + workTime + ".fasta") 
    with open(fastaPath, "a+", encoding='utf-8') as fasta_output:
        for seq in data:
            for seqName, seqCon in seq.items():
                seqLenth = len(seqCon)
            fasta_output.write(">seq_"+seqName +
                               "_"+str(seqLenth)+"\n")
            fasta_output.write(seqCon+"\n")


if __name__ == '__main__':
    seq1 = {"test1": "ATCGCTAG"}
    seq2 = {"test2": "ATCGCTAGTTCCG"}
    import time
    workTime = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
    saveFasta(workTime,seq1, seq2)
