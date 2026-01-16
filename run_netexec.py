#!/usr/bin/env python3
"""
NetExec Programmatic API

Provides run_netexec() function that captures output instead of printing.
"""
import sys
import io
import contextlib


def run_netexec(args: list[str]) -> dict:
    """
    Run NetExec with given CLI arguments and capture output.
    
    Args:
        args: List of CLI arguments (e.g., ['smb', '--help'])
    
    Returns:
        dict with keys:
            - returncode: int (0 = success)
            - stdout: str (captured output)
            - stderr: str (captured errors)
            - parsed: None (reserved for future use)
    
    Example:
        >>> result = run_netexec(['--help'])
        >>> print(result['stdout'])
    """
    result = {
        "returncode": 0,
        "stdout": "",
        "stderr": "",
        "parsed": None
    }
    
    # Save original argv
    original_argv = sys.argv.copy()
    
    # Buffers for stdout/stderr
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    
    try:
        # Set argv for netexec's argument parser
        sys.argv = ['netexec'] + list(args)
        
        # Import capture utility
        from nxc.console import OutputCapture
        
        # Capture all output
        with OutputCapture() as console_capture:
            with contextlib.redirect_stdout(stdout_buffer):
                with contextlib.redirect_stderr(stderr_buffer):
                    try:
                        # Setup and run
                        from nxc.first_run import first_run_setup
                        from nxc.logger import nxc_logger
                        from nxc.netexec import main
                        
                        first_run_setup(nxc_logger)
                        main()
                        
                    except SystemExit as e:
                        # Capture exit code (--help exits with 1)
                        result["returncode"] = e.code if isinstance(e.code, int) else 0
                    except Exception as e:
                        result["returncode"] = 1
                        stderr_buffer.write(f"Error: {e}\n")
        
        # Combine captured outputs
        result["stdout"] = console_capture.get_output() + stdout_buffer.getvalue()
        result["stderr"] = stderr_buffer.getvalue()
        
    finally:
        # Restore original argv
        sys.argv = original_argv
    
    return result


def run_self_test():
    """Quick self-test to verify the API works."""
    print("=" * 50)
    print("run_netexec() API Test")
    print("=" * 50)
    
    # Test 1: --help
    print("\n[TEST 1] Calling run_netexec(['--help'])")
    result = run_netexec(['--help'])
    print(f"  Return code: {result['returncode']}")
    print(f"  Output length: {len(result['stdout'])} chars")
    print(f"  Has content: {'YES' if len(result['stdout']) > 100 else 'NO'}")
    
    # Test 2: smb --help
    print("\n[TEST 2] Calling run_netexec(['smb', '--help'])")
    result = run_netexec(['smb', '--help'])
    print(f"  Return code: {result['returncode']}")
    print(f"  Output length: {len(result['stdout'])} chars")
    
    # Test 3: Show captured output sample
    print("\n[TEST 3] Sample of captured output:")
    print("-" * 50)
    print(result['stdout'][:500] if result['stdout'] else "(empty)")
    print("-" * 50)
    
    # Test 4: Verify no stdout leak
    print("\n[TEST 4] Verify output was captured (not printed directly)")
    print("  If you see NetExec banner ABOVE this line = FAIL")
    print("  If output only in 'Sample' section above = PASS")
    
    print("\n" + "=" * 50)
    print("Tests complete!")
    print("=" * 50)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != '--self-test':
        # Pass through to netexec
        from nxc.netexec import main
        main()
    else:
        run_self_test()
