#!/usr/bin/env python3

import argparse

import meshio


def write_veg_with_material(
    input_mesh_file: str,
    output_veg_file: str,
    density: float,
    young_modulus: float,
    poisson_ratio: float,
) -> None:
    mesh = meshio.read(input_mesh_file)
    vertices = mesh.points

    tetrahedra = None
    for cell_block in mesh.cells:
        if cell_block.type == "tetra":
            tetrahedra = cell_block.data
            break

    if tetrahedra is None:
        raise RuntimeError(f"No tetrahedral elements found in {input_mesh_file}.")

    num_vertices = len(vertices)
    num_tets = len(tetrahedra)

    with open(output_veg_file, "w", encoding="utf-8") as f:
        f.write("# Vega mesh file.\n")
        f.write(f"# {num_vertices} vertices, {num_tets} elements\n\n")

        f.write("*VERTICES\n")
        f.write(f"{num_vertices} 3 0 0\n")
        for i, v in enumerate(vertices, start=1):
            f.write(f"{i} {v[0]} {v[1]} {v[2]}\n")

        f.write("\n*ELEMENTS\n")
        f.write("TET\n")
        f.write(f"{num_tets} 4 0\n")
        for i, tet in enumerate(tetrahedra, start=1):
            f.write(f"{i} {tet[0] + 1} {tet[1] + 1} {tet[2] + 1} {tet[3] + 1}\n")

        f.write("\n*MATERIAL defaultMat\n")
        f.write(f"ENU, {density:g}, {young_modulus:g}, {poisson_ratio:g}\n\n")
        f.write("*REGION\n")
        f.write("allElements, defaultMat\n")

    print(f"Wrote Vega mesh: {output_veg_file}")
    print(
        f"Material: ENU, density={density:g}, E={young_modulus:g}, nu={poisson_ratio:g}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert tetrahedral .mesh to Vega .veg.")
    parser.add_argument("input_mesh", help="Input tetrahedral mesh (e.g., Medit .mesh)")
    parser.add_argument("output_veg", help="Output Vega .veg mesh")
    parser.add_argument(
        "--density",
        type=float,
        default=1000.0,
        help="Material density (default: 1000)",
    )
    parser.add_argument(
        "--young",
        type=float,
        default=8.0e7,
        help="Young's modulus E (default: 8e7)",
    )
    parser.add_argument(
        "--nu",
        type=float,
        default=0.35,
        help="Poisson ratio nu (default: 0.35)",
    )
    args = parser.parse_args()

    write_veg_with_material(
        args.input_mesh, args.output_veg, args.density, args.young, args.nu
    )


if __name__ == "__main__":
    main()
