#!/usr/bin/env python3
"""
Comprehensive Multi-Domain PCI Controls Test Suite

Tests:
1. Controls catalog loading and resolution
2. New policy packs (pci-secure-software, pci-tokenization)
3. Control metadata resolution in violations
4. Cross-domain framework mapping
5. Integration with existing checks
"""

import json
import os
import sys
from pathlib import Path

# Add comp_leo to path
sys.path.insert(0, str(Path(__file__).parent))

def test_catalog_loading():
    """Test 1: Verify controls catalog loads correctly"""
    print("=" * 70)
    print("TEST 1: Controls Catalog Loading")
    print("=" * 70)
    
    try:
        from comp_leo.policies.catalog import get_control, reset_cache
        
        # Reset cache for clean test
        reset_cache()
        
        # Test loading a control
        control = get_control("SECURE-01-01")
        
        if control:
            print("✅ Catalog loaded successfully")
            print(f"   Control ID: {control.get('Control_ID')}")
            print(f"   Standard: {control.get('Standard_Name')}")
            print(f"   Section: {control.get('Section_Title')}")
            print(f"   Domain: {control.get('Domain')}")
            print(f"   Description: {control.get('Requirement_Description')[:60]}...")
            return True
        else:
            print("❌ Control not found in catalog")
            return False
            
    except Exception as e:
        print(f"❌ Catalog loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_policy_packs_exist():
    """Test 2: Verify new policy packs exist and are valid"""
    print("\n" + "=" * 70)
    print("TEST 2: Policy Packs Validation")
    print("=" * 70)
    
    policies_dir = Path(__file__).parent / "comp_leo" / "policies"
    
    required_policies = [
        "pci-dss-basic.json",
        "pci-dss-standard.json",
        "pci-secure-software.json",
        "pci-tokenization.json"
    ]
    
    all_valid = True
    
    for policy_file in required_policies:
        policy_path = policies_dir / policy_file
        
        if not policy_path.exists():
            print(f"❌ Missing: {policy_file}")
            all_valid = False
            continue
        
        try:
            with open(policy_path, 'r') as f:
                policy = json.load(f)
            
            # Validate structure
            required_fields = ["name", "rules", "framework", "threshold"]
            missing = [f for f in required_fields if f not in policy]
            
            if missing:
                print(f"❌ {policy_file}: Missing fields {missing}")
                all_valid = False
            else:
                print(f"✅ {policy_file}: Valid")
                print(f"   Name: {policy['name']}")
                print(f"   Framework: {policy['framework']}")
                print(f"   Rules: {len(policy['rules'])}")
                print(f"   Threshold: {policy['threshold']}")
                
        except Exception as e:
            print(f"❌ {policy_file}: Parse error - {e}")
            all_valid = False
    
    return all_valid


def test_control_resolution():
    """Test 3: Test control metadata resolution in violation creation"""
    print("\n" + "=" * 70)
    print("TEST 3: Control Metadata Resolution")
    print("=" * 70)
    
    try:
        from comp_leo.policies.catalog import get_control
        
        # Test multiple control IDs across domains
        test_controls = [
            "SECURE-01-01",  # Secure Software
            "SECURE-06-03",  # Cryptography
            "TOKEN-03-01",   # Tokenization
            "PCI-DSS-0210",  # PCI DSS Core
        ]
        
        all_resolved = True
        
        for control_id in test_controls:
            control = get_control(control_id)
            
            if control:
                print(f"✅ {control_id} resolved:")
                print(f"   Framework: {control.get('Standard_Name', 'N/A')}")
                print(f"   Section: {control.get('Section_Title', 'N/A')}")
                print(f"   Domain: {control.get('Domain', 'N/A')}")
            else:
                print(f"❌ {control_id} NOT found in catalog")
                all_resolved = False
        
        return all_resolved
        
    except Exception as e:
        print(f"❌ Control resolution failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_violation_with_controls():
    """Test 4: Test violation creation with control mapping"""
    print("\n" + "=" * 70)
    print("TEST 4: Violation Control Mapping")
    print("=" * 70)
    
    try:
        from comp_leo.core.models import ControlMapping
        from comp_leo.policies.catalog import get_control
        
        # Simulate violation creation with control resolution
        test_control_id = "SECURE-06-03"
        control = get_control(test_control_id)
        
        if not control:
            print(f"❌ Control {test_control_id} not in catalog")
            return False
        
        # Create ControlMapping as the checker would
        framework = control.get("Standard_Name") or control.get("Domain") or "PCI"
        control_name = control.get("Section_Title") or control.get("Requirement_Ref") or test_control_id
        description = control.get("Requirement_Description") or ""
        
        mapping = ControlMapping(
            framework=framework,
            control_id=test_control_id,
            control_name=control_name,
            description=description
        )
        
        print("✅ ControlMapping created successfully:")
        print(f"   Framework: {mapping.framework}")
        print(f"   Control ID: {mapping.control_id}")
        print(f"   Control Name: {mapping.control_name}")
        print(f"   Description: {mapping.description[:60]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Violation mapping failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_policy_control_references():
    """Test 5: Verify policy rules reference valid controls"""
    print("\n" + "=" * 70)
    print("TEST 5: Policy Control References")
    print("=" * 70)
    
    try:
        from comp_leo.policies.catalog import get_control
        
        policies_dir = Path(__file__).parent / "comp_leo" / "policies"
        
        test_policies = [
            "pci-secure-software.json",
            "pci-tokenization.json"
        ]
        
        all_valid = True
        
        for policy_file in test_policies:
            policy_path = policies_dir / policy_file
            
            with open(policy_path, 'r') as f:
                policy = json.load(f)
            
            print(f"\n📋 {policy['name']}:")
            
            total_controls = 0
            valid_controls = 0
            invalid_controls = []
            
            for rule in policy.get('rules', []):
                controls = rule.get('controls', [])
                total_controls += len(controls)
                
                for control_id in controls:
                    if isinstance(control_id, str):
                        control = get_control(control_id)
                        if control:
                            valid_controls += 1
                        else:
                            invalid_controls.append(control_id)
            
            if invalid_controls:
                print(f"   ⚠️  {len(invalid_controls)} controls not in catalog:")
                for cid in invalid_controls[:5]:  # Show first 5
                    print(f"      - {cid}")
                all_valid = False
            else:
                print(f"   ✅ All {valid_controls} control references valid")
        
        return all_valid
        
    except Exception as e:
        print(f"❌ Policy validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_end_to_end_scan():
    """Test 6: End-to-end scan with new policies"""
    print("\n" + "=" * 70)
    print("TEST 6: End-to-End Policy Scan Simulation")
    print("=" * 70)
    
    try:
        # Load a policy
        policies_dir = Path(__file__).parent / "comp_leo" / "policies"
        policy_path = policies_dir / "pci-secure-software.json"
        
        with open(policy_path, 'r') as f:
            policy = json.load(f)
        
        print(f"✅ Loaded policy: {policy['name']}")
        print(f"   Rules: {len(policy['rules'])}")
        
        # Simulate checking controls in first rule
        first_rule = policy['rules'][0]
        print(f"\n📋 Testing rule: {first_rule['name']}")
        print(f"   Controls: {len(first_rule.get('controls', []))}")
        
        from comp_leo.policies.catalog import get_control
        
        for control_id in first_rule.get('controls', [])[:3]:  # Test first 3
            control = get_control(control_id)
            if control:
                print(f"   ✅ {control_id}: {control.get('Section_Title', 'N/A')}")
            else:
                print(f"   ❌ {control_id}: NOT FOUND")
        
        return True
        
    except Exception as e:
        print(f"❌ End-to-end test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_catalog_stats():
    """Test 7: Catalog statistics and coverage"""
    print("\n" + "=" * 70)
    print("TEST 7: Catalog Statistics")
    print("=" * 70)
    
    try:
        catalog_path = Path(__file__).parent / "comp_leo" / "policies" / "controls_catalog.json"
        
        with open(catalog_path, 'r') as f:
            catalog = json.load(f)
        
        controls = catalog.get('controls', [])
        
        print(f"📊 Catalog Statistics:")
        print(f"   Total Controls: {len(controls)}")
        
        # Count by standard
        standards = {}
        domains = {}
        
        for control in controls:
            std = control.get('Standard_Name', 'Unknown')
            dom = control.get('Domain', 'Unknown')
            
            standards[std] = standards.get(std, 0) + 1
            domains[dom] = domains.get(dom, 0) + 1
        
        print(f"\n   By Standard:")
        for std, count in sorted(standards.items()):
            print(f"      - {std}: {count}")
        
        print(f"\n   By Domain:")
        for dom, count in sorted(domains.items())[:10]:  # Top 10
            print(f"      - {dom}: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Stats generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "🔍" * 35)
    print("MULTI-DOMAIN PCI CONTROLS - COMPREHENSIVE TEST SUITE")
    print("🔍" * 35 + "\n")
    
    tests = [
        ("Catalog Loading", test_catalog_loading),
        ("Policy Packs Validation", test_policy_packs_exist),
        ("Control Resolution", test_control_resolution),
        ("Violation Control Mapping", test_violation_with_controls),
        ("Policy Control References", test_policy_control_references),
        ("End-to-End Scan", test_end_to_end_scan),
        ("Catalog Statistics", test_catalog_stats),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'=' * 70}")
    print(f"OVERALL: {passed}/{total} tests passed ({passed*100//total}%)")
    print(f"{'=' * 70}\n")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Multi-domain PCI controls are working perfectly!")
        return 0
    else:
        print(f"⚠️  {total - passed} test(s) failed. Review output above.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
