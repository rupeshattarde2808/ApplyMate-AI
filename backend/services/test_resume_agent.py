import json
import sys

from agents.resume_agent import analyze_resume


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python -m services.test_resume_agent "
            "path_to_resume.pdf"
        )
        raise SystemExit(1)

    profile = analyze_resume(sys.argv[1])

    print(json.dumps(
        profile.model_dump(),
        indent=4,
        ensure_ascii=False,
    ))