# IMPORTS
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio import SearchIO

# FUNCOES

def get_prot(id):
    '''
    id= codigo da proteina a pesquisar na base de dados Swiss-Prot;
    '''
    from Bio import ExPASy
    with ExPASy.get_sprot_raw(id) as handle:
        seq_record = SeqIO.read(handle, "swiss")
    print(seq_record.seq)
    print(len(seq_record.seq), 'aa')
    for k, v in seq_record.annotations.items():
        print(k, v)
    tam= len(seq_record.seq)
    seq= seq_record.seq
    tax= seq_record.annotations["taxonomy"]
    org= seq_record.annotations["organism"]
    #host= seq_record.annotations["organism_host"]
    y = ('ID:' + id + '|' + 'SEQUENCE:' + seq + '|' + 'SEQUENCE LENGTH:' + str(tam) + 'bp' + '|' + 'TAXONOMY:' + str(tax) + '|' + 'ORGANISM:' + org )
    return y

def filtro(seq):
    seq = seq.split('|')
    return seq

def blast_prot(FILE, seq):
    result_handle = NCBIWWW.qblast('blastp', 'nr', seq)
    with open(FILE, "w") as out_handle:
        out_handle.write(result_handle.read())
    result_handle.close()

def parse(file, E_VALUE_THRESH):
    result_handle = open(file)
    blast_record = NCBIXML.read(result_handle)
    FILE = []
    if E_VALUE_THRESH == None:
        E_VALUE_THRESH = 0.05
    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            if hsp.expect < E_VALUE_THRESH:
                y = alignment.title + '|' + str(alignment.length) + '|' + str(hsp.expect)
                FILE.append(y)
    return FILE

def isol_AC(x):
    DicAC = {}
    for hit in x:
        c = []
        for y in range(len(hit)):
            if hit[y] == '|':
                c.append(y)
        type = hit[0: c[0]]
        if type == "gb":
            k = hit[c[0]+1 : c[1]]
            if k not in DicAC:
                DicAC[k] = 1
    ListAC = list(DicAC.keys())
    return ListAC

def proteico(id,file,blast = False, E_VALUE_THRESH = None):
    if blast == True:
        x = get_prot(id)
        print(x)
        seq = filtro(x)
        print(seq)
        blast_prot(file, seq[1])
    x = get_prot(id)
    print(x)
    x = parse(file, E_VALUE_THRESH)
    print(x)
    ListAC = isol_AC(x)
    print(ListAC)
    with open('id_list_prot.txt', 'w') as f:
        for item in ListAC:
            f.write("%s\n" % item)

proteico("P02679","P02679_blast.xml" ,False, None)


def parse_prot(file):
    result_handle = open(file)
    from Bio.Blast import NCBIXML
    blast_record = NCBIXML.read(result_handle)
    E_VALUE_THRESH = 0.04
    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            if hsp.expect < E_VALUE_THRESH:
                print("****Alignment****")
                print("sequence:", alignment.title)
                print("length:", alignment.length)
                print("e value:", hsp.expect)
                print(hsp.query[0:75] + "...")
                print(hsp.match[0:75] + "...")
                print(hsp.sbjct[0:75] + "...")
    from Bio import SearchIO
    blast_qresult = SearchIO.read(file, "blast-xml")
    print(blast_qresult)
    result_handle.close()


parse_prot("P02679_blast.xml")


# CHAMADAS
# bio_prot('ORF3a.gb', 'genbank')
# blast_prot('ORF3a.gb', 'gb', 'ORF3a_blast.xml')
# blast_prot_pars('ORF3a_blast.xml')
# get_prot('P02675', True)
#blast_prot('P0DTC3', "PROT_ORF3a_blast1.xml")
#blast_prot_pars("PROT_ORF3a_blast.xml")
