import sys

toggle_sol_code = """
        function toggleSol(btn) {
            const solBox = btn.nextElementSibling;
            if (solBox.style.display === 'none') {
                solBox.style.display = 'block';
                btn.innerHTML = '❌ ĐÓNG LỜI GIẢI';
            } else {
                solBox.style.display = 'none';
                btn.innerHTML = '🔍 HIỆN LỜI GIẢI';
            }
        }
        function updateTimerDisplay() {"""

files = [
    r'c:\Users\huyds\OneDrive\2. PARA\1 - Projects\CaChep_Ecosystem\02_Distribution\List_Captoc_Web\01_Kho_De_Goc\CT_02.html',
    r'c:\Users\huyds\OneDrive\2. PARA\1 - Projects\CaChep_Ecosystem\01_Factory\Test_Web\20250515_CT_02\03_Outputs\02_Unified.html'
]

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if "function toggleSol" not in content:
        content = content.replace("        function updateTimerDisplay() {", toggle_sol_code)
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)

print("toggleSol function injected successfully!")
