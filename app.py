import argparse
from decimal import Decimal, InvalidOperation

# Factors to base units: meter (distance) and gram (mass)
UNITS = {
    "distance": {"m": Decimal("1"), "km": Decimal("1000"), "cm": Decimal("0.01"), "mi": Decimal("1609.344"), "ft": Decimal("0.3048")},
    "mass": {"g": Decimal("1"), "kg": Decimal("1000"), "lb": Decimal("453.59237"), "oz": Decimal("28.349523125")},
}


def convert(value, source, target):
    try:
        value = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError("Value must be numeric") from exc
    if not value.is_finite():
        raise ValueError("Value must be finite")
    source, target = source.lower(), target.lower()
    temperatures = {"c", "f", "k"}
    if source in temperatures and target in temperatures:
        kelvin = {"c": lambda x: x + Decimal("273.15"),
                  "f": lambda x: (x - 32) * Decimal(5) / 9 + Decimal("273.15"),
                  "k": lambda x: x}[source](value)
        if kelvin < 0:
            raise ValueError("Temperature cannot be below absolute zero")
        return {"c": lambda x: x - Decimal("273.15"),
                "f": lambda x: (x - Decimal("273.15")) * 9 / 5 + 32,
                "k": lambda x: x}[target](kelvin)
    for group in UNITS.values():
        if source in group and target in group:
            return value * group[source] / group[target]
    raise ValueError("Unsupported or incompatible units")


def main():
    parser = argparse.ArgumentParser(description="Unit converter")
    parser.add_argument("value")
    parser.add_argument("source", help="From unit: c, f, k, m, km, cm, mi, ft, g, kg, lb, oz")
    parser.add_argument("target", help="To unit")
    args = parser.parse_args()
    try:
        result = convert(args.value, args.source, args.target)
        print(f"{args.value} {args.source} = {result:.6f} {args.target}")
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
