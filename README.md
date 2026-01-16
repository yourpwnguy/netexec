# NetExec Nuitka Compilation Task - Submission

## About This Submission

Hi! This is my attempt at the NetExec Nuitka compilation task. I want to be upfront, I didn't complete everything, but I learned a lot and want to document what I did, what I struggled with, and what I would do differently with more time.

---

## What Was The Task?

The goal was to:
1. Create a `run_netexec()` function that runs NetExec programmatically and captures output (instead of printing to console)
2. Make the binary path-independent (works from any folder)
3. Compile everything into a single .exe using Nuitka
4. Add a self-test that runs when the exe launches

---

## What I Actually Completed

### The `run_netexec()` API

This is the main thing I focused on. I created a function that:
- Takes CLI arguments as a list
- Runs NetExec internally
- Captures all output and returns it as a dictionary
- Does NOT print anything to stdout during execution

**How to use it:**

```python
from run_netexec import run_netexec

# Run any netexec command
result = run_netexec(['smb', '192.168.1.1', '-u', 'admin', '-p', 'password'])

# Check the result
print(result['returncode'])  # 0 means success
print(result['stdout'])       # All the output that would have been printed
print(result['stderr'])       # Any errors

# What it returns 

```json
{
    "returncode": 0,          # Exit code
    "stdout": "...",          # Captured output
    "stderr": "...",          # Captured errors
    "parsed": None            # Reserved for future use
}
```

### Basic Self-Test

I added a simple self-test that verifies the API works:

```bash
python run_netexec.py
```

This runs a few checks:

- Calls run_netexec(['--help']) and verifies output is captured
- Calls run_netexec(['smb', '--help']) for protocol-specific test
- Shows a sample of captured output
- Verifies nothing leaked to stdout

### Files I Modified/Created

New Files:
`run_netexec.py` (in repo root)

- Contains the run_netexec() function
- Contains run_self_test() function
- This would be the entry point for Nuitka compilation

Modified Files:
`nxc/console.py`

Original was just:

```python
from rich.console import Console
nxc_console = Console(soft_wrap=True, tab_size=4)
```

I changed it to use a CapturableConsole class that can redirect output to a buffer when needed. The tricky part was that NetExec uses Rich library for pretty output, so I couldn't just capture stdout - I had to intercept at the Rich Console level.

### How The Output Capture Works
This took me a while to figure out. NetExec prints output in multiple ways:

- Rich Console - The pretty formatted output (colors, tables, etc.)
- Python print() - Some direct prints
- Logging - Debug/error messages

My solution:

1. Save original sys.argv
2. Set sys.argv to netexec + user args
3. Start OutputCapture (for Rich console)
4. Redirect stdout/stderr to StringIO
5. Run netexec main()
6. Catch SystemExit (--help does this)
7. Collect all captured text
8. Restore original sys.argv
9. Return result dict

### What I Did NOT Complete

I want to be honest about what's missing:

❌ Nuitka Compilation

I wrote a build.py script but didn't successfully compile the final binary even at the last moment (Although, I fixed it but didn't had time for a re-run to verify it). Now, the compilation process kept running into issues:

- Memory issues - Nuitka's --show-memory flag caused crashes initially which was solved later
- Build time - Each attempt took more than 1 hour, making debugging slow and this was my main issue while working on this assignment.
- Python 3.13 - I was using Python 3.13 which might have compatibility issues with Nuitka, which I really don't know, as I compiling other python programs, and they were successful.

The build script is there (build.py) in the root of repo, and should work in theory, but I couldn't verify the final .exe works correctly.

❌ Full Path Independence

The task asked for the binary to work from any directory without needing external files. I started working on this in nxc/paths.py but due to compilation problems and constraints, I had to drop this at the final memoments. Working solution is better than broken one.

My idea was actually simple: 

- Runtime data (logs, databases) goes to ~/.nxc/ (user's home)
- Bundled data (configs, scripts) gets embedded in the exe
- The code detects if it's running compiled or in development mode through Nutika embedded attributes.

❌ Proper Video Demo

Without a working compiled binary, I couldn't make the demo video showing it running on a clean Windows VM.

### How To Test What I Did

You don't need to compile anything to test the API:

```bash
# 1. Clone and setup
git clone github.com/yourpwnguy/netexec
cd NetExec

# 2. Initialise virtual env using python package manager
py -3.13 -m venv .venv   
.venv\Scripts\activate  

# 3. Install dependencies
pip install -e .

# 4. Run the self-test
python run_netexec.py
```

You should see output like:

```
==================================================
run_netexec() API Test
==================================================

[TEST 1] Calling run_netexec(['--help'])
  Return code: 0
  Output length: 2297 chars
  Has content: YES

[TEST 2] Calling run_netexec(['smb', '--help'])
  Return code: 0
  Output length: 13363 chars

[TEST 3] Sample of captured output:
--------------------------------------------------
usage: netexec smb [-h] [--version] [-t THREADS] [--timeout TIMEOUT] [--jitter INTERVAL] [--no-progress] [--log LOG]
                   [--verbose | --debug] [-6] [--dns-server DNS_SERVER] [--dns-tcp] [--dns-timeout DNS_TIMEOUT]
                   [-u USERNAME [USERNAME ...]] [-p PASSWORD [PASSWORD ...]] [-id CRED_ID [CRED_ID ...]] [--ignore-pw-decoding]
                   [--no-bruteforce] [--continue-on-success] [--gfail-limit LIMIT] [--ufail-limit LIMIT] [--fail-limit LIMIT]

--------------------------------------------------

[TEST 4] Verify output was captured (not printed directly)
  If you see NetExec banner ABOVE this line = FAIL
  If output only in 'Sample' section above = PASS

==================================================
Tests complete!
==================================================
```
The return code being 1 for --help is normal, argparse exits with code 1 after showing help.

### If I Had More Time

- Path Independence - I would have worked on path independence.
- Handle edge cases - Unicode paths, permission errors, etc.

### What I Learned

Even though I didn't finish everything, I learned:

- Rich library internals - How Rich Console works and how to intercept its output
- Nuitka basics - How onefile mode works, data bundling, package inclusion
- NetExec architecture - How the codebase is structured, how protocols/modules work
- Context managers - Used them for clean output capture

### Build Instructions (For Reference)

If you want to try compiling:

```bash
# Install requirements
pip install nuitka ordered-set

# Run build script
python build.py
```

### Final Thoughts

I know this isn't a complete submission. The task was ambitious and I underestimated how long the Nuitka compilation would take to debug. I spent a lot of time on the output capture mechanism because I thought that was the core technical challenge, but then ran out of time for the compilation part. This took me centuries to compile. Although on the positive side, I actually got more info on Nutika for how to speed up the compilation process. The author was talking about his utility which runs a hinting process. Anyways, that's for some other time as it's not related.

If nothing else, the run_netexec() API does work and demonstrates the concept of capturing NetExec output programmatically. You can test it right now without any compilation.

Thanks for considering my submission. Even if I don't move forward, this was a good learning experience.
