class ZebraProxySdk {
  constructor(baseUrl = "http://127.0.0.1:5000") {
    this.baseUrl = baseUrl;
  }

  async _request(endpoint, { method = "GET", body, params } = {}) {
    let url = `${this.baseUrl}${endpoint}`;
    if (params) {
      const qs = new URLSearchParams(params).toString();
      if (qs) url += `?${qs}`;
    }
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined
    });

    if (!res.ok) {
      throw new Error(`API Error ${res.status}: ${await res.text()}`);
    }

    return res.json();
  }

  async listPrinters() {
    try {
      return await this._request("/printers");
    } catch (error) {
      console.error("Failed to list printers:", error);
      return { success: false, error: error.message };
    }
  }

  async getDefaultPrinter() {
    try {
      return await this._request("/printers/default");
    } catch (error) {
      console.error("Failed to get default printer:", error);
      return { success: false, error: error.message };
    }
  }

  async setDefaultPrinter(id) {
    try {
      return await this._request("/printers/default", {
        method: "POST",
        body: { id }
      });
    } catch (error) {
      console.error("Failed to set default printer:", error);
      return { success: false, error: error.message };
    }
  }

  async printZPL(zpl, printer_id = null) {
    try {
      const payload = { zpl };
      if (printer_id) payload.printer_id = printer_id;
      return await this._request("/print", {
        method: "POST",
        body: payload
      });
    } catch (error) {
      console.error("Failed to print ZPL:", error);
      return { success: false, error: error.message };
    }
  }

  async getStatus(printer_id = null) {
    try {
      return await this._request("/status", {
        params: printer_id ? { printer_id } : {}
      });
    } catch (error) {
      console.error("Failed to get printer status:", error);
      return { success: false, error: error.message };
    }
  }
}
