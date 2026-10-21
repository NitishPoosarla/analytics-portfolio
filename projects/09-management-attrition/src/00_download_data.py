"""09-management-attrition — download IBM HR Analytics Employee Attrition (public mirror).

Source mirror: nelson-wu/employee-attrition-ml on GitHub; 1,470 employees,
35 columns, no real PII.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from shared.utils import download   # noqa: E402

PROJECT = Path(__file__).resolve().parent.parent
URL = ("https://raw.githubusercontent.com/nelson-wu/employee-attrition-ml/"
       "master/WA_Fn-UseC_-HR-Employee-Attrition.csv")


def main() -> None:
    (PROJECT / "data" / "raw").mkdir(parents=True, exist_ok=True)
    download(URL, PROJECT / "data" / "raw" / "hr_attrition.csv", "IBM HR attrition")


if __name__ == "__main__":
    main()
