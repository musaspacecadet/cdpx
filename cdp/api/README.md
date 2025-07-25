## Generated CDP API Wrappers

These classes provide an object-oriented, blocking wrapper around the base CDP commands.

Instantiate them individually with a client object conforming to the `CDPClient` protocol (defined in `../util.py`), or use the aggregated `DevTools` from the main package.

Example (Individual API):
```python
from cdp.api import PageAPI
from cdp import CDPClient
from my_cdp_client import MyClient # Your implementation of CDPClient

client: CDPClient = MyClient(...)
page_api = PageAPI(client)

result = page_api.navigate(url='https://example.com')
print(f'Navigation frame ID: {result}') # Example output
```

Example (Aggregated Client):
```python
from cdp import DevTools, CDPClient
from my_cdp_client import MyClient # Your implementation of CDPClient

client_impl: CDPClient = MyClient(...)
cdp = DevTools(client_impl)

frame_id = cdp.page.navigate(url='https://example.com')
cookies = cdp.network.get_all_cookies()
print(f'Frame: {frame_id}, Cookies: {len(cookies)}')
```
