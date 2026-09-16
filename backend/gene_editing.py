import re

class GeneEditorPrototype:
    def __init__(self, target_dna: str):
        # Enforce uppercase string representing a DNA sequence
        self.dna = target_dna.upper()
        
    def find_crispr_guides(self) -> list:
        """
        Scans DNA sequence for SpCas9 PAM sites (NGG).
        Returns a list of dictionaries with 20nt guide sequences and positions.
        """
        guides = []
        # Regex looks for 20 bases followed by 'GG' (matching the NGG PAM site on the 3' end)
        # Using lookahead to handle overlapping sites safely
        pam_pattern = re.compile(r'(?=([ATCG]{20})[ATCG]GG)')
        
        for match in pam_pattern.finditer(self.dna):
            guide_seq = match.group(1)
            # The exact position where the 20nt guide starts
            start_pos = match.start()
            guides.append({
                "guide_rna": guide_seq.replace('T', 'U'), # Convert DNA guide to RNA representation
                "dna_target": guide_seq,
                "start_index": start_pos,
                "cut_site": start_pos + 17 # Cas9 cuts roughly 3bp upstream of the PAM site
            })
        return guides

    def simulate_nhej_knockout(self, cut_site: int, deletion_length: int = 1) -> str:
        """
        Simulates an error-prone DNA repair (NHEJ) causing a framing mutation.
        Deletes a user-specified number of bases at the cut site.
        """
        if cut_site < 0 or cut_site >= len(self.dna):
            raise ValueError("Cut site is out of sequence bounds.")
            
        # Splice out the deleted sequence to mock an error-prone cellular repair
        edited_dna = self.dna[:cut_site] + self.dna[cut_site + deletion_length:]
        return edited_dna

# ==========================================
# PROTOTYPE EXECUTION
# ==========================================
if __name__ == "__main__":
    # A sample genome string containing target zones
    sample_gene = "ATCGATCGAATCGATCGATCGATCGTGCATGCATGGCTAGCTAGCTAG"
    print(f"Original Sequence ({len(sample_gene)} bp): {sample_gene}\n")
    
    # Initialize the programmatic system
    editor = GeneEditorPrototype(sample_gene)
    
    # 1. Discover potential CRISPR RNA guides
    available_guides = editor.find_crispr_guides()
    print(f"🔬 Found {len(available_guides)} potential Cas9 target guide(s):")
    
    for idx, guide in enumerate(available_guides, 1):
        print(f"  [{idx}] Guide RNA (5'->3'): {guide['guide_rna']}")
        print(f"      Target Index Start: {guide['start_index']} | Predicted Cut Site: {guide['cut_site']}")
        
    # 2. Pick the first guide and execute a programmatic knockout simulation
    if available_guides:
        chosen_target = available_guides[0]
        print(f"\n⚡ Executing Simulated CRISPR Cut at position {chosen_target['cut_site']}...")
        
        # Simulate a 1-base deletion knockout
        mutated_sequence = editor.simulate_nhej_knockout(cut_site=chosen_target['cut_site'], deletion_length=1)
        print(f"Edited Sequence   ({len(mutated_sequence)} bp): {mutated_sequence}")
        print("Result: Frame-shift knockout successfully modeled.")
