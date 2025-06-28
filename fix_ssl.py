#!/usr/bin/env python
"""
SSL Certificate Fix and Diagnostic Tool

This script provides comprehensive SSL certificate fixes and diagnostics for YouTube Summarizer.
It includes:
1. Diagnostic checks for SSL connections
2. Certificate updates and fixes
3. macOS-specific fixes
"""

import os
import sys
import ssl
import urllib.request
import subprocess
import json

def test_ssl_connections():
    """Test SSL connections to essential services"""
    print("\n=== Testing SSL Connections ===")
    
    sites = [
        "https://www.google.com",
        "https://www.youtube.com",
        "https://ai.google.dev/",
    ]
    
    results = {}
    for site in sites:
        print(f"Testing connection to {site}...")
        try:
            with urllib.request.urlopen(site) as response:
                results[site] = response.status == 200
                if results[site]:
                    print(f"✅ Successfully connected to {site}")
                else:
                    print(f"❌ Failed to connect to {site} - Status: {response.status}")
        except Exception as e:
            results[site] = False
            print(f"❌ Error connecting to {site}: {str(e)}")
    
    return all(results.values())

def update_certifi():
    """Update the certifi package"""
    print("\n=== Updating SSL Certificates ===")
    try:
        import certifi
        print(f"Current certifi path: {certifi.where()}")
        
        # Try to upgrade certifi
        print("Upgrading certifi package...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "certifi"])
        print("✅ certifi package upgraded successfully")
        
        # Return the updated certifi path
        import certifi
        return certifi.where()
    except Exception as e:
        print(f"❌ Failed to update certifi: {str(e)}")
        return None

def fix_macos_certificates():
    """Apply macOS-specific certificate fixes"""
    if not (os.name == 'posix' and hasattr(os, 'uname') and os.uname().sysname == 'Darwin'):
        print("Not a macOS system, skipping macOS-specific fixes.")
        return False
    
    print("\n=== Applying macOS Certificate Fixes ===")
    
    # Get Python version
    python_version = '.'.join(sys.version.split(' ')[0].split('.')[:2])
    print(f"Detected Python version: {python_version}")
    
    # Find macOS certificate command
    cert_cmd_paths = [
        f"/Applications/Python {python_version}/Install Certificates.command",
        f"/Applications/Python.app/Contents/MacOS/Install Certificates.command",
    ]
    
    cert_cmd = None
    for path in cert_cmd_paths:
        if os.path.exists(path):
            cert_cmd = path
            break
    
    if cert_cmd:
        print(f"Found certificate installation command: {cert_cmd}")
        try:
            print("Executing certificate installation...")
            os.chmod(cert_cmd, 0o755)  # Make executable
            subprocess.check_call([cert_cmd])
            print("✅ macOS certificates installed successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to install certificates: {str(e)}")
    else:
        print("⚠️ Certificate installation command not found")
    
    return False

def setup_environment_variables(cert_path):
    """Set up environment variables for SSL certificates"""
    if not cert_path:
        return
    
    print("\n=== Setting Up Environment Variables ===")
    
    # Set environment variables for the current process
    os.environ['SSL_CERT_FILE'] = cert_path
    os.environ['REQUESTS_CA_BUNDLE'] = cert_path
    print(f"Set SSL_CERT_FILE and REQUESTS_CA_BUNDLE to {cert_path}")
    
    # Create script content to set these variables
    script_content = f"""# Add these lines to your shell profile (.bashrc, .zshrc, etc.)
export SSL_CERT_FILE={cert_path}
export REQUESTS_CA_BUNDLE={cert_path}
"""
    
    # Save to a file
    with open('ssl_env_vars.sh', 'w') as f:
        f.write(script_content)
    
    print("Environment variable setup saved to ssl_env_vars.sh")
    print("To make these permanent, run:")
    print("  cat ssl_env_vars.sh >> ~/.zshrc  # For zsh")
    print("  # OR")
    print("  cat ssl_env_vars.sh >> ~/.bash_profile  # For bash")

def apply_code_fixes():
    """Show code fixes that can be applied"""
    print("\n=== Code Fixes for SSL Issues ===")
    
    print("Add these lines to the top of your scripts that make HTTPS requests:")
    print("""
import ssl

# Method 1: Best practice - use certifi
try:
    import certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl._create_default_https_context = lambda: ssl_context
except ImportError:
    # Method 2: Less secure fallback - use unverified context
    ssl._create_default_https_context = ssl._create_unverified_context
""")

def main():
    print("=" * 60)
    print("SSL Certificate Fix and Diagnostic Tool")
    print("=" * 60)
    
    # Step 1: Test connections
    connections_ok = test_ssl_connections()
    
    # Step 2: Update certifi
    cert_path = update_certifi()
    
    # Step 3: Apply macOS fixes if needed
    if not connections_ok and os.name == 'posix' and hasattr(os, 'uname') and os.uname().sysname == 'Darwin':
        fix_macos_certificates()
    
    # Step 4: Set up environment variables
    setup_environment_variables(cert_path)
    
    # Step 5: Show code fixes
    apply_code_fixes()
    
    # Step 6: Final test
    print("\n=== Final SSL Connection Test ===")
    final_test = test_ssl_connections()
    
    print("\n" + "=" * 60)
    if final_test:
        print("✅ SSL configuration is now working correctly!")
    else:
        print("⚠️ SSL issues may still exist. As a last resort, you can use:")
        print("ssl._create_default_https_context = ssl._create_unverified_context")
        print("(Note: This reduces security and should only be used for testing)")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
