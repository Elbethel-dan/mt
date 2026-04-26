# debug_data.py
import sys
from pathlib import Path

def check_file(filepath, name):
    print(f"\n{'='*50}")
    print(f"Checking {name}: {filepath}")
    print(f"{'='*50}")
    
    if not Path(filepath).exists():
        print(f"❌ FILE NOT FOUND!")
        print(f"   Looked for: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"✅ Total lines: {len(lines)}")
    
    # Check first 3 non-empty lines
    non_empty = [l for l in lines if l.strip()]
    print(f"\nFirst 3 non-empty lines:")
    for i, line in enumerate(non_empty[:3]):
        words = line.strip().split()
        print(f"  {i+1}. [{len(words)} words] {line.strip()[:100]}...")
    
    # Sample statistics
    if non_empty:
        lengths = [len(l.strip().split()) for l in non_empty[:1000]]
        print(f"\nStats (first 1000 lines):")
        print(f"  Avg words: {sum(lengths)/len(lengths):.1f}")
        print(f"  Min words: {min(lengths)}")
        print(f"  Max words: {max(lengths)}")
    
    return True

# ============================================
# UPDATE THESE PATHS TO WHERE YOUR FILES ARE
# ============================================
RAW_EN = "/Users/elbethelzewdie/Downloads/Telegram Lite/el-workspace/el-workspace/data/raw/English.en"   # Change this to your English file path
RAW_AM = "/Users/elbethelzewdie/Downloads/Telegram Lite/el-workspace/el-workspace/data/raw/Amharic.am"   # Change this to your Amharic file path
# ============================================

print("\n🔍 ENGLISH-AMHARIC DATA DIAGNOSTIC\n")

# Check if files exist
if not Path(RAW_EN).exists():
    print(f"❌ English file not found at: {RAW_EN}")
    print(f"\nCurrent directory: {Path.cwd()}")
    print("Files in current directory:")
    for f in Path.cwd().iterdir():
        if f.is_file():
            print(f"  - {f.name}")
    sys.exit(1)

check_file(RAW_EN, "ENGLISH (Source)")
check_file(RAW_AM, "AMHARIC (Target)")

# Check alignment
if Path(RAW_EN).exists() and Path(RAW_AM).exists():
    with open(RAW_EN, 'r', encoding='utf-8') as f:
        en_lines = f.readlines()
    with open(RAW_AM, 'r', encoding='utf-8') as f:
        am_lines = f.readlines()
    
    print(f"\n{'='*50}")
    print("ALIGNMENT CHECK")
    print(f"{'='*50}")
    print(f"English lines: {len(en_lines)}")
    print(f"Amharic lines: {len(am_lines)}")
    
    if len(en_lines) != len(am_lines):
        print(f"❌ MISMATCH! Files have different line counts!")
        print(f"   Difference: {abs(len(en_lines) - len(am_lines))} lines")
    else:
        print(f"✅ Lines are aligned ({len(en_lines)} pairs)")
        
        # Show first aligned pair
        print(f"\nFirst sentence pair:")
        print(f"EN: {en_lines[0].strip()[:150]}")
        print(f"AM: {am_lines[0].strip()[:150]}")