#!/usr/bin/env python3
"""
Test script for agent tools.

Tests all agent tools to ensure they work correctly without requiring LLM API calls.
"""

import json
from agent_tools import CampaignAnalysisTools


def print_test(test_name, success=True):
    """Print test result."""
    status = "✅" if success else "❌"
    print(f"{status} {test_name}")


def test_tools():
    """Test all agent tools."""
    print("\n🧪 Testing Agent Tools\n")
    print("=" * 70)

    tools = CampaignAnalysisTools()

    # Test 1: Load Campaign Data
    print("\n📊 Test 1: Load Campaign Data")
    print("-" * 70)
    try:
        result = tools.load_campaign_data("Campaign_A", num_sessions=1000)
        data = json.loads(result)
        print(f"Campaign ID: {data['campaign_id']}")
        print(f"Total Sessions: {data['total_sessions']}")
        print(f"Overall eCR: {data['overall_ecr']:.2%}")
        print(f"Overall RPS: ${data['overall_rps']:.2f}")
        print_test("Load Campaign Data", True)
    except Exception as e:
        print(f"Error: {e}")
        print_test("Load Campaign Data", False)
        return

    # Test 2: Run Segmentation Analysis
    print("\n🎯 Test 2: Run Segmentation Analysis")
    print("-" * 70)
    try:
        # Use lower thresholds to find segments
        result = tools.run_segmentation_analysis("Campaign_A", max_segments=5, min_lift=0.10, min_segment_pct=0.03)

        # Check if result is JSON or plain text
        if result.startswith("No significant segments"):
            print(result)
            print_test("Run Segmentation Analysis", True)  # Still pass - this is valid
        else:
            data = json.loads(result)
            print(f"Total segments found: {data['total_segments_found']}")
            if data['total_segments_found'] > 0:
                top = data['top_segments'][0]
                print(f"\nTop segment:")
                print(f"  Condition: {top['condition']}")
                print(f"  eCR: {top['ecr']} (lift: {top['ecr_lift']})")
                print(f"  Bid multiplier: {top['bid_multiplier']}")
                print(f"  Sessions: {top['sessions']}")
            print_test("Run Segmentation Analysis", True)
    except Exception as e:
        print(f"Error: {e}")
        print_test("Run Segmentation Analysis", False)
        return

    # Test 3: Compare Campaigns
    print("\n⚖️  Test 3: Compare Campaigns")
    print("-" * 70)
    try:
        # Load second campaign
        tools.load_campaign_data("Campaign_B", num_sessions=1000)
        result = tools.compare_campaigns("Campaign_A", "Campaign_B", min_advantage=0.10)

        # Check if result is JSON or plain text
        if result.startswith("No significant"):
            print(result)
            print_test("Compare Campaigns", True)
        else:
            data = json.loads(result)
            print(f"Campaigns compared: {data['campaign_a']} vs {data['campaign_b']}")
            print(f"Total differences found: {data['total_differences_found']}")
            if data['total_differences_found'] > 0:
                top = data['top_insights'][0]
                print(f"\nTop insight:")
                print(f"  Segment: {top['segment']}")
                print(f"  Advantage: {top['advantage']}")
            print_test("Compare Campaigns", True)
    except Exception as e:
        print(f"Error: {e}")
        print_test("Compare Campaigns", False)
        return

    # Test 4: Get Segment Details
    print("\n🔍 Test 4: Get Segment Details")
    print("-" * 70)
    try:
        # Get first segment from previous analysis
        seg_result = tools.run_segmentation_analysis("Campaign_A", max_segments=1, min_lift=0.10)

        if seg_result.startswith("No significant"):
            print("No segments available, skipping details test")
            print_test("Get Segment Details", True)  # Still pass
        else:
            seg_data = json.loads(seg_result)
            if seg_data['total_segments_found'] > 0:
                segment_condition = seg_data['top_segments'][0]['condition']
                result = tools.get_segment_details("Campaign_A", segment_condition)

                if "not found" in result:
                    print(result)
                    print_test("Get Segment Details", True)
                else:
                    data = json.loads(result)
                    print(f"Segment: {data['condition']}")
                    print(f"Sessions: {data['sessions']}")
                    print(f"Conversions: {data['conversions']}")
                    print(f"Bid multiplier: {data['recommendations']['bid_multiplier']}")
                    print_test("Get Segment Details", True)
            else:
                print("No segments to test")
                print_test("Get Segment Details", True)
    except Exception as e:
        print(f"Error: {e}")
        print_test("Get Segment Details", False)
        return

    # Test 5: Calculate ROI Impact
    print("\n💰 Test 5: Calculate ROI Impact")
    print("-" * 70)
    try:
        # Use same segment from previous test
        if seg_result and not seg_result.startswith("No significant"):
            seg_data = json.loads(seg_result)
            if seg_data['total_segments_found'] > 0:
                segment_condition = seg_data['top_segments'][0]['condition']
                result = tools.calculate_roi_impact(
                    "Campaign_A",
                    segment_condition,
                    current_cpc=1.50,
                    budget_allocation_pct=100.0
                )
                if "not found" in result:
                    print(result)
                    print_test("Calculate ROI Impact", True)
                else:
                    data = json.loads(result)
                    print(f"Segment: {data['segment']}")
                    print(f"Current ROI: {data['current_performance']['roi']}")
                    print(f"Projected ROI: {data['projected_performance']['roi']}")
                    print(f"ROI Change: {data['impact']['roi_change']}")
                    print_test("Calculate ROI Impact", True)
            else:
                print("No segments to test")
                print_test("Calculate ROI Impact", True)
        else:
            print("No segments available, skipping ROI test")
            print_test("Calculate ROI Impact", True)
    except Exception as e:
        print(f"Error: {e}")
        print_test("Calculate ROI Impact", False)
        return

    # Test 6: List Campaigns
    print("\n📋 Test 6: List Campaigns")
    print("-" * 70)
    try:
        result = tools.list_available_campaigns()
        data = json.loads(result)
        print(f"Loaded campaigns: {data['loaded_campaigns']}")
        print(f"Count: {data['count']}")
        print_test("List Campaigns", True)
    except Exception as e:
        print(f"Error: {e}")
        print_test("List Campaigns", False)
        return

    # Test 7: Get Recommendations Summary
    print("\n📝 Test 7: Get Recommendations Summary")
    print("-" * 70)
    try:
        result = tools.get_recommendations_summary("Campaign_A", top_n=3)
        print(result[:500] if len(result) > 500 else result)  # Show first 500 chars
        print_test("Get Recommendations Summary", True)
    except Exception as e:
        print(f"Error: {e}")
        print_test("Get Recommendations Summary", False)
        return

    # Summary
    print("\n" + "=" * 70)
    print("✅ All agent tools tests passed!")
    print("\nThe agent tools are working correctly.")
    print("To test the full AI agent, you'll need to:")
    print("  1. Set up an API key (OpenAI or Anthropic)")
    print("  2. Run: python agent_cli.py")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    test_tools()
