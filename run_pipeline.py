#!/usr/bin/env python3
"""
Simplified runner for the Exoplanet Detection Pipeline
Executes each phase separately with error handling
"""

import sys
import traceback
from pathlib import Path
import json
from datetime import datetime

def setup_environment():
    """Create necessary directories"""
    directories = [
        'data/raw', 'data/processed', 'data/augmented', 'data/synthetic', 'data/tess',
        'models', 'models/tess',
        'reports/figures', 'reports/figures/augmentation', 'reports/figures/tess',
        'reports/validation', 'reports/tess_analysis',
        'logs'
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✓ Directory structure created")

def run_phase(phase_name, code_section):
    """Run a single phase with error handling"""
    print(f"\n{'='*80}")
    print(f"RUNNING: {phase_name}")
    print('='*80 + '\n')
    
    try:
        exec(code_section, globals())
        print(f"\n✓ {phase_name} completed successfully")
        return True
    except Exception as e:
        print(f"\n✗ {phase_name} failed with error:")
        print(traceback.format_exc())
        
        # Log error
        log_file = Path('logs') / f'{phase_name.lower().replace(" ", "_")}_error.log'
        with open(log_file, 'w') as f:
            f.write(f"Error in {phase_name}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n\n")
            f.write(traceback.format_exc())
        
        return False

def main():
    """Main pipeline execution"""
    print("="*80)
    print("EXOPLANET DETECTION PIPELINE")
    print("NASA Space Apps Challenge 2025")
    print("="*80 + "\n")
    
    # Setup
    setup_environment()
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'phases': {}
    }
    
    # Load the full script
    with open('copy_of_ada.py', 'r') as f:
        full_code = f.read()
    
    # Phase 1: Data Scraping
    scraper_section = full_code[full_code.find('class NASAExoplanetScraper:'):
                                full_code.find('# ========================================================================\n# EXOPLANET HUNTER AI - EXPLORATORY')]
    
    if run_phase("Data Scraping", scraper_section):
        results['phases']['data_scraping'] = 'success'
    else:
        results['phases']['data_scraping'] = 'failed'
        print("\n⚠️ Data scraping failed, but continuing with pipeline...")
    
    # Check if data exists
    if not Path('data/raw').exists() or not list(Path('data/raw').glob('*.csv')):
        print("\n⚠️ Warning: No raw data found. Some phases may fail.")
    
    # Phase 2: EDA (if data exists)
    if Path('data/raw/kepler_cumulative.csv').exists():
        print("\n✓ Raw data found, proceeding with EDA")
        # Note: EDA section is complex, may need manual extraction
        results['phases']['eda'] = 'skipped - requires manual review'
    else:
        print("\n⚠️ Skipping EDA - no data available")
        results['phases']['eda'] = 'skipped - no data'
    
    # Save results
    with open('pipeline_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*80)
    print("PIPELINE EXECUTION COMPLETE")
    print("="*80)
    print(f"\nResults saved to: pipeline_results.json")
    print(f"Logs saved to: logs/")
    
    # Print summary
    print("\nPhase Summary:")
    for phase, status in results['phases'].items():
        status_icon = "✓" if status == "success" else "⚠️"
        print(f"  {status_icon} {phase}: {status}")

if __name__ == "__main__":
    main()
