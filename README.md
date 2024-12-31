 # Name that Car!
## Video Demo:  https://www.youtube.com/watch?v=h29giKFCnBY&feature=youtu.be

## Inspiration
    This is a game I developed for my son who is crazy about cars. I got the idea after perusing the CS50 Python Gallery of Final Projects and coming across an insect guessing game. The premise of the game is to identify the name of the insect when shown a limited area of an image. Incorrect guesses will reveal larger and larger areas of the picture. I thought this idea nicely encapsulated the skills I had learnt during the course and would also prove to be a big hit with my son as we often try to guess the make of oncoming vehicles when driving (my son is such a motorhead that he is able to identify the make of oncoming cars even before their badge is visible as he is able to recognise their shape!)

## Project Files
    project.py
    test_project.py
    requirements.txt
    README.md

## Implementation
### Program
    I decided to split the program into three functions, one for each of the three main parts of the game: scraping appropriate images from the net, selecting a random image, and the actual gameplay which involved five guesses where every incorrect guess reveals another random part of the image. According to lecture recommendations, I kept constant values at the top of the programme and added docstrings to each function.

    scrape_images(url)
    The goal of scrape_images(url) was to scrape images from the Robb Report's article about the 50 Greatest Sports Cars of all Time. This website was selected as it had a wide variety of high quality images of sports cars which were nicely labelled. I used BeautifulSoup4 to contact the website and find all the image tags in the HTML, using regex to select images with a resolution of 1024w because larger images were not as common, and smaller images were not as enjoyable to look at. I used the alt attribute to label the images, replacing unsafe characters with underscores to make suitable filenames. After screening by the filename to filter out undesirable/irrelevant images, I then downloaded the images into a local folder. Since this process takes about 10 seconds, I also included a warning message to the user.

    random_pic(designated_folder)
    Python's os module was used to create a list of the names of the files in the specified folder with the choice() method from Python's random module used to select and return the name of one of the images.

    guess(folder_name_cars,chosen_pic)
    Users were given five guesses to correctly identify the make and/or model in the given image. The selected car image was overlaid with a mask which had a randomly located transparent square and each incorrect answer replaced the mask with the addition of another randomly located transparent square. A transparent square 200 pixels on each side was found to provide the ideal difficulty, and the location of the squares was restricted in order to ensure the entire square was located within the image frame. These locations were kept in a list and this was iterated over before each guess to produce the mask. Regex was used to extract the make and model of the car from the filename in order to reveal the correct answer to the user. If users provide invalid answers (empty strings or fewer than three characters), they are prompted to provide a valid guess without the attempt being consumed or an additional area of the image being revealed. If the user guesses the make and/or model correctly, the entire image is revealed with a congratulatory message, along with the make and model of the vehicle. If the user fails to correctly guess the make and/or model within 5 attempts, the entire image is revealed with a consolation message, along with the correct make and model of the vehicle.


    After completing these functions and producing a working prototype, I realized why developers favour a test-driven approach as writing unit tests for the web-scraping proved difficult and I eventually had to create an additional function to assist with this.

    count_images(folder)
    This function simply counts the number of files in the designated folder. It was used as a helper function to assist in the testing of scrape_images(url).

### Unit Tests
    def test_scrape_images()
    Writing a unit test for the web-scraping function proved difficult so I decided to create a helper function (count_images(folder)) to check the number of images downloaded.

    test_random_pic()
    I didn't know how to create a mock website with a curated image so I simply included the creation of a test folder with a known image as part of the scrape_images(url) function. Since this folder only had one image, the random_pic(designated_folder) function could then be successfully tested.

    test_guess()
    The exit type and value of this function was tested with both valid and invalid input as well as five incorrect guesses. io.StringIO was used to simulate a user's guess.

## Work-ons
    Create smaller, more modular functions
    Implement a test-driven approach
    Investigate mocking in pytest
