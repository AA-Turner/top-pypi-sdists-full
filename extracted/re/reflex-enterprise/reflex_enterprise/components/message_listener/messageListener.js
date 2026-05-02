import { useEffect } from "react";

export function MessageListener({ allowedOrigin, onMessage, filterAttributes }) {
  useEffect(() => {
    window.addEventListener("message", (event) => {
      if (event.origin !== allowedOrigin) {
        return;
      }
      if (filterAttributes) {
        for (const [key, regex_str] of Object.entries(filterAttributes)) {
          const regex = new RegExp(regex_str);
          if (!regex.test(event.data[key])) {
            return;
          }
        }
      }
      onMessage({
        origin: event.origin,
        data: event.data,
        timestamp: event.timeStamp,
      });
    });
    return () => {
      window.removeEventListener("message", onMessage);
    };
  }, [allowedOrigin, onMessage, filterAttributes]);

  return null;
}
