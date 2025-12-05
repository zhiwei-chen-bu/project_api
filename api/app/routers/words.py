from fastapi import APIRouter
import random

router = APIRouter()

WORDS = [
    {
        "word_level" : "Intermediate",
        "word": "Advertisement",
        "meaning": "a notice or announcement in a public medium promoting a product, service, or event or publicizing a job vacancy.",
        "example": "He learned about the job from an advertisement in the newspaper.",
    },
    {
        "word_level" : "Advanced",
        "word": "Candidate",
        "meaning": "a person who applies for a job or other position or is nominated for election.",
        "example": "The Democratic candidate is leading in the polls.",
    },
    {
        "word_level" : "Beginner",
        "word": "Elevator",
        "meaning": "a platform or compartment housed in a shaft for raising and lowering people or things to different floors or levels.",
        "example": "We took the elevator to the 10th floor.",
    },
    {
        "word_level" : "Advanced",
        "word": "Generation",
        "meaning": "all of the people born and living at about the same time, regarded collectively.",
        "example": "This new phone is the latest generation of smartphones.",
    },
    {
        "word_level" : "Beginner",
        "word": "Rain",
        "meaning": "moisture condensed from the atmosphere that falls visibly in separate drops.",
        "example": "We're expecting a lot of rain this weekend.",
    },
    {
        "word_level" : "Intermediate",
        "word": "Vacation",
        "meaning": "an extended period of leisure and recreation, especially one spent away from home or in traveling.",
        "example": "We are planning a vacation to Italy next summer.",
    },
]

@router.get("/word")
async def get_random_word():
    return random.choice(WORDS)
