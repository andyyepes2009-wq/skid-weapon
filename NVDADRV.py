import wmi

def get_recommended_driver(gpu_name):
    driver_map = {
        "210": "2.210", "220": "2.220", "230": "2.230", "240": "2.240", 
        "250": "2.250", "260": "2.260", "275": "2.275", "280": "2.280", "285": "2.285", "295": "2.295",
        "460": "4.460", "465": "4.465", "470": "4.470", "480": "4.480",
        "550": "5.550", "560": "5.560", "570": "5.570", "580": "5.580", "590": "5.590",
        "650": "6.650", "660": "6.660", "670": "6.670", "680": "6.680", "690": "6.690",
        "750": "7.750", "760": "7.760", "770": "7.770", "780": "7.780",
        "950": "9.950", "960": "9.960", "970": "9.970", "980": "9.980",
        "1050": "10.1050", "1060": "10.1060", "1070": "10.1070", "1080": "10.1080",
        "2050": "2.205", "2060": "2.206", "2070": "2.207", "2080": "2.208",
        "3050": "3.305", "3060": "3.306", "3070": "3.307", "3080": "3.308", "3090": "3.309",
        "4050": "4.405", "4060": "4.406", "4070": "4.407", "4080": "4.408", "4090": "4.409",
        "5050": "5.505", "5060": "5.506", "5070": "5.507", "5080": "5.508", "5090": "5.509"
    }
    sorted_models = sorted(driver_map.keys(), key=len, reverse=True)
    for model in sorted_models:
        if model in gpu_name:
            base_driver = driver_map[model]
            if "TI" in gpu_name.upper():
                return f"{base_driver}.5"
                
            return base_driver
            
    return None
def search_nvidia_drivers():
    print("-==-=================================-==-")
    print("         NVIDIA DRIVER SEARCH            ")
    print("=================---====================")
    try:
        w = wmi.WMI()
        gpus = w.Win32_VideoController()
        found_nvidia = False
        for gpu in gpus:
            name = gpu.Name
            if "NVIDIA" in name.upper():
                found_nvidia = True
                recommended = get_recommended_driver(name)
                if recommended:
                    print(f"Required Driver Version: {recommended}")
                else:
                    print("No specific custom driver mapped for this model.")
        if not found_nvidia:
            print("\nNo NVIDIA hardware detected.")
    except Exception as e:
        print(f"Error accessing hardware data: {e}")
        
    print("\n=========================================")

if __name__ == "__main__":
    search_nvidia_drivers()
    input("\nPress Enter to exit...")