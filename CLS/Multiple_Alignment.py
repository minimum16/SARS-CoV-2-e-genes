from Bio.Align.Applications import ClustalwCommandline

class Mutiple:
    def __ini__(self, dir, in_file):
        self.diretoria= dir
        self.in_file = in_file

    def alignment(self):
        clustalw_cline = ClustalwCommandline(self.diretoria, infile= self.in_file)
        clustalw_cline()
        print(clustalw_cline)
