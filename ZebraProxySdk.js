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

  async selectDefaultPrinter() {
    try {
      const printers = await this.listPrinters();
      if (!printers || printers.length === 0) {
        alert("No printers found.");
        return;
      }

      const selectedPrinter = await this._showPrinterDialog(printers);
      if (selectedPrinter) {
        await this.setDefaultPrinter(selectedPrinter);
        alert(`Default printer set to: ${selectedPrinter}`);
      }
    } catch (error) {
      console.error("Error selecting default printer:", error);
    }
  }

  _showPrinterDialog(printers) {
    return new Promise((resolve) => {
      const dialog = document.createElement("div");
      dialog.style.position = "fixed";
      dialog.style.top = "50%";
      dialog.style.left = "50%";
      dialog.style.transform = "translate(-50%, -50%)";
      dialog.style.background = "white";
      dialog.style.padding = "20px";
      dialog.style.boxShadow = "0 0 10px rgba(0,0,0,0.3)";
      dialog.style.zIndex = "1000";

      const label = document.createElement("label");
      label.innerText = "Select a printer:";
      dialog.appendChild(label);

      const select = document.createElement("select");
      printers.forEach((printer) => {
        const option = document.createElement("option");
        option.value = printer.id;
        option.textContent = printer.id;
        select.appendChild(option);
      });
      dialog.appendChild(select);

      const button = document.createElement("button");
      button.innerText = "Set Default";
      button.style.marginLeft = "10px";
      button.onclick = () => {
        resolve(select.value);
        document.body.removeChild(dialog);
      };

      dialog.appendChild(button);
      document.body.appendChild(dialog);
    });
  }
}
