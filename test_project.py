import pytest
import sys
import io
from project import random_pic, guess, scrape_images, count_images

# Constants
CAR_IMAGES_FOLDER = "car_images"
TEST_FOLDER = "car_images_test"

def test_scrape_images():
    assert(scrape_images("https://robbreport.com/motors/cars/lists/the-50-greatest-sports-cars-of-all-time-1235871704/")) == "Image downloading and naming completed!"
    assert(count_images(CAR_IMAGES_FOLDER)) == 34
    
def test_random_pic(): 
    assert(random_pic(TEST_FOLDER)) == "Nissan Skyline GT-R.jpg"

def test_guess_invalid():
    with pytest.raises(SystemExit) as excinfo:
        guess(CAR_IMAGES_FOLDER, "there_is_no_car")
    assert excinfo.type == SystemExit
    assert excinfo.value.code == "Image does not exist" 

def test_guess_valid():
    sys.stdin = io.StringIO("Nissan\n")
    with pytest.raises(SystemExit) as excinfo:
        guess(TEST_FOLDER, "Nissan Skyline GT-R.jpg")
    assert excinfo.type == SystemExit
    assert excinfo.value.code == "Great work! You are correct! The car was a Nissan Skyline.\nYou are a walking encyclopedia of car brands!"

def test_guess_valid_but_incorrect():
    sys.stdin = io.StringIO("Zonda\nFerrari\nBMW\nTesla\nFord\n")
    with pytest.raises(SystemExit) as excinfo:
        guess(TEST_FOLDER, "Nissan Skyline GT-R.jpg")
    assert excinfo.type == SystemExit
    assert excinfo.value.code == "Your five attempts are up. The car was a Nissan Skyline.\nBetter luck next time."
       