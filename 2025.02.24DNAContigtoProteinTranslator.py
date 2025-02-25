import os 
os.system("clear")
print("Welcome to the DNA contig Translator")

from itertools import permutations

# DNA to protein translation table by single letter code
DNA_CODON_TABLE = {
    "ATA": "I", "ATC": "I", "ATT": "I", "ATG": "M",
    "ACA": "T", "ACC": "T", "ACG": "T", "ACT": "T",
    "AAC": "N", "AAT": "N", "AAA": "K", "AAG": "K",
    "AGC": "S", "AGT": "S", "AGA": "R", "AGG": "R",
    "CTA": "L", "CTC": "L", "CTG": "L", "CTT": "L",
    "CCA": "P", "CCC": "P", "CCG": "P", "CCT": "P",
    "CAC": "H", "CAT": "H", "CAA": "Q", "CAG": "Q",
    "CGA": "R", "CGC": "R", "CGG": "R", "CGT": "R",
    "GTA": "V", "GTC": "V", "GTG": "V", "GTT": "V",
    "GCA": "A", "GCC": "A", "GCG": "A", "GCT": "A",
    "GAC": "D", "GAT": "D", "GAA": "E", "GAG": "E",
    "GGA": "G", "GGC": "G", "GGG": "G", "GGT": "G",
    "TCA": "S", "TCC": "S", "TCG": "S", "TCT": "S",
    "TTC": "F", "TTT": "F", "TTA": "L", "TTG": "L",
    "TAC": "Y", "TAT": "Y", "TAA": "*", "TAG": "*",
    "TGC": "C", "TGT": "C", "TGA": "*", "TGG": "W"
}

def find_overlap(seq1, seq2, min_overlap=3):
    """Find the maximum overlap between the suffix of seq1 and the prefix of seq2."""
    max_overlap = 0
    merged_seq = None

    for i in range(min_overlap, len(seq1)):  # Start from min_overlap
        if seq2.startswith(seq1[i:]):  # Check if suffix of seq1 matches prefix of seq2
            max_overlap = len(seq1) - i
            merged_seq = seq1 + seq2[max_overlap:]
            break  # Stop at the first (largest) overlap found
    
    return max_overlap, merged_seq

def assemble_sequences(sequences, min_overlap=3):
    """Iteratively merge sequences based on overlaps until no more merging is possible."""
    while len(sequences) > 1:
        best_pair = None
        best_merged_seq = None
        best_overlap = 0

        # Check all pairwise overlaps
        for seq1, seq2 in permutations(sequences, 2):
            overlap, merged_seq = find_overlap(seq1, seq2, min_overlap)
            if overlap > best_overlap:
                best_overlap = overlap
                best_pair = (seq1, seq2)
                best_merged_seq = merged_seq

        # If no more overlaps found, stop merging
        if best_overlap == 0:
            break

        # Merge the best pair
        sequences.remove(best_pair[0])
        sequences.remove(best_pair[1])
        sequences.append(best_merged_seq)

    return sequences

def translate_to_protein(dna_sequence):
    """Translate a DNA sequence into a protein sequence using the codon table."""
    protein = ""
    for i in range(0, len(dna_sequence) - 2, 3):  # Read in triplets
        codon = dna_sequence[i:i+3]
        protein += DNA_CODON_TABLE.get(codon, "?")  # '?' for unknown codons
    return protein

# Example input: DNA sequence reads
reads = [
    "AACATTCAGAACTTT" ,
"TTTCAGCGTATGGCT" ,
"GCTACTATTTGCTCT" , 
"TCTATTTCTGCTTGG" ,
"TGGGAATCTCAGATGGAA"
]

# Step 1: Assemble contigs
assembled_contigs = assemble_sequences(reads)

# Step 2: Translate each assembled contig to protein
for contig in assembled_contigs:
    protein = translate_to_protein(contig)
    print(f"Contig: {contig}")
    print(f"Protein: {protein}")
