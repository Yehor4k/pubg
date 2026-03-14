---

# PUBG Artillery/Mortar Distance Calculator

A lightweight Python utility designed to help players calculate precise artillery distances in PUBG. By calibrating to the in-game grid, the tool provides accurate measurements from your current position to your target.


<table>
<tr>
   <td><b>Support Project</b></td>
   <td >
      <a href="https://www.paypal.com/donate/?hosted_button_id=7QQS473KE8C38"><img src="https://raw.githubusercontent.com/seerge/g-helper/main/docs/paypal-eur.png" width="150" alt="PayPal EUR"></a>&nbsp;
      <a href="https://www.paypal.com/donate/?hosted_button_id=SXNDJMPSYW4CQ"><img src="https://raw.githubusercontent.com/seerge/g-helper/main/docs/paypal-usd.png" width="150" alt="PayPal USD"></a>&nbsp;
   </td>
</tr>
</table>


## 🚀 Installation

### .exe usage

1. **Download the App**: Navigate to the [Releases](https://github.com/Yehor4k/pubg/releases/) tab and download the latest version of the executable.

2. Navigate to your Downloads folder and execute the calc.exe file.

### .py usage, aka source code

1. Install [Git](https://git-scm.com/install/windows) on your computer (optional) | Or just download the source code. Click green "<> Code" button at the top and download the .zip file | [Follow this tutorial on how to download the source code](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives#downloading-source-code-archives)

2. Install Python and in cmd install the pynput library with this command:
```bash
pip install pynput

```

3. (Follow this step only, if you installed the Git) Open your prefferable folder and copy the repository with Git via cmd:
```bash
git clone https://github.com/Yehor4k/pubg

```
Then open the cloned repository folder via this command:
```bash
cd pubg

```

4. Execute the run.py file with this command after you installed the pynput library:
```bash
py run.py

```

---

## 🎮 How to Use

The latest release has the new feature – Settings Window, which let's you tweak some settings.

![image](https://github.com/Yehor4k/pubg/blob/main/pictures/4.png)

Once the program is running, you can use the following hotkeys to measure distances:

### 1. Calibration + Measurement

**Hotkey:** `Ctrl` + `Alt` + `S`

* **Step 1**: On map hold click and drag to select a single **white grid square** (the 100x100m square) on your map to calibrate the scale.

![image](https://github.com/Yehor4k/pubg/blob/main/pictures/1.png)

* **Step 2**: Immediately hold click and drag from **your location** to your **target's location**.

![image](https://github.com/Yehor4k/pubg/blob/main/pictures/2.png)

![image](https://github.com/Yehor4k/pubg/blob/main/pictures/3.png)

### 2. Measurement Only

**Hotkey:** `Alt` + `S`

* Use this if you have already calibrated and just need a new reading.
* On map simply hold click and drag from **your location** to your **target's location**.

![image](https://github.com/Yehor4k/pubg/blob/main/pictures/2.png)

![image](https://github.com/Yehor4k/pubg/blob/main/pictures/3.png)

---

> **Tip:** For the most accurate shots, ensure your map zoom level remains consistent after calibration, or recalibrate if you zoom in/out significantly.
