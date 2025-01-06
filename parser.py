import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import xml.etree.ElementTree as ET

def decimal_degrees_to_ddm(value, is_latitude=True):
    """
    Convert decimal degrees to decimal degrees + minutes (DDM).
    Returns a string: D°MM.mmm' [N/S/E/W].
    """
    if is_latitude:
        hemisphere = 'N' if value >= 0 else 'S'
    else:
        hemisphere = 'E' if value >= 0 else 'W'
    absolute_value = abs(value)
    
    # Integer degrees
    degrees = int(absolute_value)
    # Decimal minutes
    minutes = (absolute_value - degrees) * 60
    
    return f"{degrees}°{minutes:.3f}' {hemisphere}"

def copy_column_to_clipboard(treeview, column_index):
    """
    Copies all values of the specified column index from the Treeview to the clipboard.
    """
    lines = []
    for child in treeview.get_children():
        values = treeview.item(child, 'values')
        if len(values) > column_index:
            lines.append(values[column_index])
    clipboard_text = "\n".join(lines)
    
    # Access the main window for clipboard
    root = treeview.nametowidget(treeview.winfo_parent()).master
    root.clipboard_clear()
    root.clipboard_append(clipboard_text)
    
    messagebox.showinfo("Copied", f"Copied column {column_index+1} to clipboard.")

def parse_and_populate_tree(file_path, treeview):
    """
    Parses XML at file_path, populates the Treeview with waypoint data.
    Removes 'Venom1' and newlines from the name.
    """
    # Clear existing rows
    for row in treeview.get_children():
        treeview.delete(row)

    try:
        print(f"[DEBUG] Parsing XML file: {file_path}")
        xml_tree = ET.parse(file_path)
        root = xml_tree.getroot()

        # Find all <Waypoint> elements
        for waypoint in root.findall(".//Waypoint"):
            name_el = waypoint.find("Name")
            lat_el = waypoint.find("./Position/Latitude")
            lon_el = waypoint.find("./Position/Longitude")
            alt_el = waypoint.find("./Position/Altitude")

            # If any required element is missing, skip
            if None in (name_el, lat_el, lon_el, alt_el):
                continue

            raw_name = name_el.text if name_el.text else ""
            # Remove "Venom1" and replace any newlines with spaces
            clean_name = raw_name.replace("Venom1", "").replace("\n", " ").strip()

            lat_str = lat_el.text.strip()
            lon_str = lon_el.text.strip()
            alt_str = alt_el.text.strip()

            # Convert to float
            try:
                lat = float(lat_str)
                lon = float(lon_str)
                alt = float(alt_str)
            except ValueError:
                continue  # skip if invalid float

            # Convert lat/lon to DDM
            lat_ddm = decimal_degrees_to_ddm(lat, is_latitude=True)
            lon_ddm = decimal_degrees_to_ddm(lon, is_latitude=False)

            # Insert into Treeview
            treeview.insert("", tk.END, values=(clean_name, lat_ddm, lon_ddm, f"{alt:.2f} ft"))

    except Exception as e:
        messagebox.showerror("Error", f"Failed to parse XML:\n{e}")

def open_xml_file(treeview):
    """
    Opens a file browser, parses the chosen XML, populates Treeview.
    """
    file_path = filedialog.askopenfilename(
        title="Select XML File",
        filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")]
    )
    if file_path:
        parse_and_populate_tree(file_path, treeview)

def main():
    print("[DEBUG] Entering main()...")

    window = tk.Tk()
    print("[DEBUG] Tk() window created.")

    window.title("XML Waypoint Parser")
    window.geometry("900x450")

    # Frame for the table
    frame = ttk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Treeview with columns
    columns = ("Name", "Latitude (DDM)", "Longitude (DDM)", "Altitude (ft)")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200)

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Buttons at the bottom
    btn_frame = ttk.Frame(window)
    btn_frame.pack(fill=tk.X, padx=5, pady=5)

    open_btn = ttk.Button(btn_frame, text="Open XML File", command=lambda: open_xml_file(tree))
    open_btn.pack(side=tk.LEFT, padx=5)

    # Make a copy button for each column
    for i, col in enumerate(columns):
        copy_btn = ttk.Button(btn_frame, text=f"Copy {col}",
                              command=lambda idx=i: copy_column_to_clipboard(tree, idx))
        copy_btn.pack(side=tk.LEFT, padx=5)

    print("[DEBUG] Entering mainloop...")
    window.mainloop()
    print("[DEBUG] mainloop exited.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[ERROR]", e)
