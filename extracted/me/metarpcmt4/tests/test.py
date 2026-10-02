import asyncio
from MetaRpcMT4.mt4_account import MT4Account


async def test_account_summary():
    user = 910798516
    password = "bzen2yz"
    host = "18.163.180.152"
    port = 443
    server_name = "VTMarkets-Demo"

    account = MT4Account(user=user, password=password)
    #await account.connect_by_host_port(host=host, port=port, base_chart_symbol="EURUSD")
    await account.connect_by_server_name(server_name=server_name, base_chart_symbol="EURUSD")

    summary = await account.account_summary()
    print("✅ Account summary:")
    print(summary)

    some  = await account.quote("sadfsf");

    async for tick in account.on_symbol_tick(["EURUSD", "GBPUSD", "BTCUSD"]):
        print(tick)


if __name__ == "__main__":
    asyncio.run(test_account_summary())
