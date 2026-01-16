#!/usr/bin/env python3
"""
Nuitka Build Script for NetExec
Produces a single-file Windows executable.
"""
import subprocess
import sys
import os
import shutil
from pathlib import Path


def get_data_args():
    """Generate data inclusion arguments."""
    args = []
    data_path = Path('nxc/data')
    
    for f in data_path.iterdir():
        src = str(f).replace('\\', '/')
        if f.is_file() and f.name != 'nxc.ico':  # Skip icon
            args.append(f'--include-data-files={src}=nxc/data/')
        elif f.is_dir():
            args.append(f'--include-data-dir={src}=nxc/data/{f.name}')
    
    return args


def build():
    # Clean
    for d in ['dist', 'run_netexec.build', 'run_netexec.dist', 'run_netexec.onefile-build']:
        if os.path.exists(d):
            shutil.rmtree(d)
    
    os.makedirs('dist', exist_ok=True)
    
    cmd = [
        sys.executable, '-m', 'nuitka',
        '--onefile',
        '--output-filename=netexec.exe',
        '--output-dir=dist',
        '--low-memory',
        '--windows-console-mode=force',
        '--onefile-no-compression',
        '--include-package=nxc',
        '--include-package=impacket',
        '--include-package=pypykatz',
        '--include-package=lsassy',
        '--include-package=dploot',
        '--include-package=certipy',
        '--include-package=aardwolf',
        '--include-package=asyauth',
        '--include-package=minikerberos',
        '--include-package=bloodhound',
        '--include-package=masky',
        '--include-package=dsinternals',
        '--include-package=paramiko',
        '--include-package=pypsrp',
        '--include-package=neo4j',
        '--include-package=rich',
        '--include-package=sqlalchemy',
        '--include-package=termcolor',
        '--include-package=requests',
        '--include-package=bs4',
        '--include-package=xmltodict',
        '--include-package=pefile',
        '--include-package=dns',
        '--include-package=cryptography',
        '--include-package=certifi',
        '--include-package=argcomplete',
        '--include-package-data=nxc',
        '--include-package-data=impacket',
        '--include-package-data=certifi',
        '--show-progress',
        'run_netexec.py',
    ]
    
    cmd.extend(get_data_args())
    
    print("Building NetExec...")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print(f"\nSUCCESS: dist/netexec.exe")
    else:
        print("\nFAILED")
        sys.exit(1)


if __name__ == '__main__':
    build()
