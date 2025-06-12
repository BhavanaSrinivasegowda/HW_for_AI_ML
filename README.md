## 📁 Folder Structure

Final\_project/                  # Main GA implementation and results
├── main\_code/                 # Python and Verilog mutation code with cocotb test
├── openlane\_synthesis/        # OpenLane setup for hardware synthesis
├── results\_pics/              # Python output graph and screenshots

Main\_Project/
└── main\_project/
└── mutation\_project1/
└── env/              # Virtual environment (lib64 shown)

Week1/ to Week9/               # Weekly design and ML/AI hardware challenges
week8\_Challenge25/             # SPI benchmark challenge
Recommendation Letter.docx     # Final recommendation document


## 💡 How to Use

### Final Genetic Algorithm Project
- Run Python: `python GA1_pyhton_main_code.py`
- Run cocotb test: `source cocotb-env/bin/activate && make`
- Run synthesis: `nix develop && openlane config.json` (inside `openlane_synthesis/`)

### Weekly Challenges
Each `WeekX/` folder contains design or coding exercises with corresponding `.docx` writeups and code (where applicable).

## ✅ Highlights
- Hardware-accelerated Genetic Algorithm (mutation block)
- Cocotb verification and OpenLane synthesis
- Q-learning FSM implementation (Week 3)
- SPI benchmarking (Week 8)
