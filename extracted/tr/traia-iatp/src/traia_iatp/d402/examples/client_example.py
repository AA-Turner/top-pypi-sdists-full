"""Example: Client agent making payments to utility agents."""

import os
import asyncio
from traia_iatp.client import create_d402_a2a_client


async def example_simple_payment():
    """Example 1: Simple payment to a utility agent."""
    print("=" * 60)
    print("Example 1: Simple Payment")
    print("=" * 60)
    
    # Create client with payment support
    client = create_d402_a2a_client(
        agent_endpoint="https://sentiment-agent.traia.io",
        payment_private_key=os.getenv("CLIENT_PRIVATE_KEY"),
        max_payment_usd=5.0  # Maximum $5 per request
    )
    
    # Send message - automatically handles payment if required
    try:
        response = await client.send_message_with_payment(
            "Analyze sentiment: 'Tech stocks rally on strong earnings'"
        )
        print(f"Response: {response}")
    except ValueError as e:
        print(f"Payment error: {e}")
    except Exception as e:
        print(f"Error: {e}")


async def example_crewai_integration():
    """Example 2: Using paid agents in CrewAI."""
    print("\n" + "=" * 60)
    print("Example 2: CrewAI Integration with Paid Agents")
    print("=" * 60)
    
    from crewai import Agent, Task, Crew
    from traia_iatp.client.crewai_a2a_tools import A2AToolkit
    from traia_iatp.registry.iatp_search_api import find_utility_agent
    
    # Find the utility agent
    agent_info = find_utility_agent(agent_id="finbert-sentiment-agent")
    
    if not agent_info:
        print("Agent not found in registry")
        return
    
    print(f"Found agent: {agent_info.name}")
    print(f"D402 Enabled: {agent_info.d402_enabled}")
    
    # Create tool with payment support
    sentiment_tool = A2AToolkit.create_tool_from_endpoint(
        endpoint=agent_info.base_url,
        name=agent_info.name,
        description=agent_info.description,
        # Payment configuration
        payment_private_key=os.getenv("CLIENT_PRIVATE_KEY"),
        max_payment_usd=1.0
    )
    
    # Create CrewAI agent
    analyst = Agent(
        role="Financial Sentiment Analyst",
        goal="Analyze sentiment of financial news",
        backstory="Expert financial analyst with access to AI sentiment tools",
        tools=[sentiment_tool],
        verbose=True
    )
    
    # Create task
    task = Task(
        description="Analyze sentiment of: 'Federal Reserve signals rate cuts ahead'",
        expected_output="Sentiment analysis with confidence scores",
        agent=analyst
    )
    
    # Run crew
    crew = Crew(agents=[analyst], tasks=[task])
    result = crew.kickoff()
    
    print(f"\nResult: {result}")


async def example_multiple_agents():
    """Example 3: Using multiple paid utility agents."""
    print("\n" + "=" * 60)
    print("Example 3: Multiple Paid Agents")
    print("=" * 60)
    
    from traia_iatp.registry.iatp_search_api import search_utility_agents
    from traia_iatp.client import create_d402_a2a_client
    
    # Search for sentiment analysis agents
    agents = search_utility_agents(
        query="sentiment analysis",
        limit=5
    )
    
    print(f"Found {len(agents)} sentiment analysis agents")
    
    # Filter for paid agents
    paid_agents = [a for a in agents if a.d402_enabled]
    print(f"Found {len(paid_agents)} paid agents")
    
    # Create clients for each paid agent
    for agent_info in paid_agents[:2]:  # Try first 2
        print(f"\n--- Testing {agent_info.name} ---")
        
        client = create_d402_a2a_client(
            agent_endpoint=agent_info.base_url,
            payment_private_key=os.getenv("CLIENT_PRIVATE_KEY"),
            max_payment_usd=1.0
        )
        
        try:
            response = await client.send_message_with_payment(
                "Analyze: 'Stock market reaches all-time high'"
            )
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")


async def example_payment_limits():
    """Example 4: Payment limits and error handling."""
    print("\n" + "=" * 60)
    print("Example 4: Payment Limits and Error Handling")
    print("=" * 60)
    
    # Create client with very low payment limit
    client = create_d402_a2a_client(
        agent_endpoint="https://expensive-agent.traia.io",
        payment_private_key=os.getenv("CLIENT_PRIVATE_KEY"),
        max_payment_usd=0.001  # Only allow $0.001
    )
    
    try:
        response = await client.send_message_with_payment("test")
        print(f"Response: {response}")
    except ValueError as e:
        print(f"Payment rejected: {e}")
        print("Solution: Increase max_payment_usd or choose a cheaper agent")


async def example_check_agent_pricing():
    """Example 5: Check agent pricing before calling."""
    print("\n" + "=" * 60)
    print("Example 5: Check Pricing Before Calling")
    print("=" * 60)
    
    from traia_iatp.registry.iatp_search_api import find_utility_agent
    
    # Find agent and check pricing
    agent_info = find_utility_agent(agent_id="finbert-sentiment-agent")
    
    if agent_info and agent_info.d402_enabled:
        payment_info = agent_info.d402_payment_info
        
        print(f"Agent: {agent_info.name}")
        print(f"D402 Enabled: {agent_info.d402_enabled}")
        
        if payment_info:
            default_price = payment_info.get("defaultPrice", {})
            print(f"Default Price: ${default_price.get('usdAmount', 'N/A')} USD")
            print(f"Network: {default_price.get('network', 'N/A')}")
            print(f"Asset: {default_price.get('asset', 'N/A')}")
            
            skill_prices = payment_info.get("skillPrices", {})
            if skill_prices:
                print("\nSkill-specific pricing:")
                for skill_id, price in skill_prices.items():
                    print(f"  {skill_id}: ${price.get('usdAmount', 'N/A')} USD")


async def main():
    """Run all examples."""
    # Example 1: Simple payment
    await example_simple_payment()
    
    # Example 2: CrewAI integration
    await example_crewai_integration()
    
    # Example 3: Multiple agents
    await example_multiple_agents()
    
    # Example 4: Payment limits
    await example_payment_limits()
    
    # Example 5: Check pricing
    await example_check_agent_pricing()


if __name__ == "__main__":
    asyncio.run(main())

