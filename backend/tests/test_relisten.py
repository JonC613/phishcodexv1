from app import relisten


def test_normalize_title_basic():
    assert relisten.normalize_title("Tweezer") == "tweezer"
    assert relisten.normalize_title("Tweezer!") == "tweezer"
    assert relisten.normalize_title(" Tweezer  ") == "tweezer"


def test_normalize_title_complex():
    assert relisten.normalize_title("Reba ->") == "reba"
    assert relisten.normalize_title("Down With Disease") == "downwithdisease"
