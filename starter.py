import time
from core.client import DevToolsClient, get_devtools_urls
from core.launch import Launcher
from cdp import DevTools
import cdp
from base64 import b64decode

url = "https://google-gruyere.appspot.com/357140325993465202745855253526428127608/"

def main():
    launcher: Launcher | None = None
    try:
        # --- Launch browser and setup DevTools connections ---
        launcher = Launcher()
        launcher.launch()
        browser_ws_url = launcher.get_websocket_url()

        client_conn = DevToolsClient(browser_ws_url)
        browser_devtools = DevTools(client_conn)

        target_id = browser_devtools.target.create_target("google.com")
        ws_url, front_url = get_devtools_urls(browser_ws_url, target_id)

        target_client = DevToolsClient(ws_url)
        target_devtools = DevTools(target_client)

        # --- Define Event Handlers ---

        def on_dom_updated(event: cdp.dom.DocumentUpdated):
            print("[DOM Updated]")

        def on_console_log(event: cdp.runtime.ConsoleAPICalled):
            print(f"[Console] {event.type.name.upper()}:")
            for arg in event.args:
                print(" ", arg.value)

        def on_js_exception(event: cdp.runtime.ExceptionThrown):
            print("[JS Exception]", event.exception_details.text)

        def on_script_parsed(event: cdp.debugger.ScriptParsed):
            if event.script_language == cdp.debugger.ScriptLanguage.JAVA_SCRIPT:
                print("[JS Script Parsed]", event.url or "<inline>")
                return True
            return False

        def on_request(event: cdp.network.RequestWillBeSent):
            print(f"[Request] {event.request.method} {event.request.url}")

        def on_response(event: cdp.network.ResponseReceived):
            print(f"[Response] {event.response.status} {event.response.url}")

        # --- Enable CDP Domains ---
        target_devtools.network.enable()
        target_devtools.debugger.enable()
        target_devtools.dom.enable()
        target_devtools.runtime.enable()
        target_devtools.log.enable()
        target_devtools.page.enable()

        # --- Attach Listeners ---
        target_client.add_event_listener(cdp.dom.DocumentUpdated, on_dom_updated)
        target_client.add_event_listener(cdp.runtime.ConsoleAPICalled, on_console_log)
        target_client.add_event_listener(cdp.runtime.ExceptionThrown, on_js_exception)
        target_client.add_event_listener(cdp.network.RequestWillBeSent, on_request)
        target_client.add_event_listener(cdp.network.ResponseReceived, on_response)

        # --- Navigate to the page ---
        target_devtools.page.navigate(url)

        # --- Wait for JavaScript to be parsed ---
        event = target_client.wait_for_event_where(cdp.debugger.ScriptParsed, on_script_parsed)

        # --- Dump JS Source ---
        source, bytecode = target_devtools.debugger.get_script_source(event.script_id)
        print("\n--- JavaScript Source ---\n")
        print(source[:1000] + "\n...")  # Print only the first 1000 chars

        # --- Evaluate expression in runtime ---
        result, exception = target_devtools.runtime.evaluate(expression='document.title')
        print("[Page Title]", result.value)

        # --- Dump the DOM ---
        root = target_devtools.dom.get_document(depth=-1)
        print("\n--- DOM Root Node ---")
        print(root.node_name, root.node_id)

        # --- Screenshot (base64 PNG) ---
        image_data = target_devtools.page.capture_screenshot()
        with open("screenshot.png", "wb") as f:
            f.write(b64decode(image_data))
        print("[Screenshot saved as screenshot.png]")

        # --- Allow time for events to fire ---
        time.sleep(3)

    finally:
        if launcher:
            print("Closing browser...")
            launcher.stop()
            print("Browser closed.")

if __name__ == "__main__":
    main()
