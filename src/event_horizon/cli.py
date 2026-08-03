import argparse
from . import tensor_alignment, batch_flux, phase_desync, field_stress

def main():
    parser = argparse.ArgumentParser(
        description="Project Event Horizon — Anomaly Diagnostics CLI"
    )
    parser.add_argument(
        "-d", "--diagnostic",
        type=int,
        choices=[1, 2, 3, 4],
        help="Run a specific diagnostic module (1: Tensor Alignment, 2: Batch Flux, 3: Phase Desync, 4: Field Stress)"
    )

    args = parser.parse_args()

    print("============================================================")
    print("      PROJECT EVENT HORIZON — NEURAL FIELD DIAGNOSTICS      ")
    print("   Station AI Safety & Forensics Unit — Dr. Michelle    ")
    print("============================================================")

    if args.diagnostic == 1:
        tensor_alignment.run_diagnostic()
    elif args.diagnostic == 2:
        batch_flux.run_diagnostic()
    elif args.diagnostic == 3:
        phase_desync.run_diagnostic()
    elif args.diagnostic == 4:
        field_stress.run_diagnostic()
    else:
        print("\nRunning full station telemetry audit (Diagnostics 01 to 04)...")
        print("\n>>> Executing Diagnostic 01: Tensor Alignment Fault...")
        tensor_alignment.run_diagnostic()

        print("\n>>> Executing Diagnostic 02: Batch Flux Instability...")
        batch_flux.run_diagnostic()

        print("\n>>> Executing Diagnostic 03: Phase Shift Desynchronization...")
        phase_desync.run_diagnostic()

        print("\n>>> Executing Diagnostic 04: Containment Field Stress Audit...")
        field_stress.run_diagnostic()

    print("\n[COMPLETE] Telemetry diagnostic sequence finished.")


if __name__ == "__main__":
    main()
