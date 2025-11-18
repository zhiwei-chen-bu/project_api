from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, get_word_by_id
from app.schemas import WordResponse , ValidateSentenceRequest, ValidateSentenceResponse, PracticeSubmissionResponse, PracticeSubmissionCreate
import random
from app.models import Word , PracticeSubmission
from app.utils import mock_ai_validation
from app.utils import check_sentence

router = APIRouter()



@router.get("/word", response_model=WordResponse)
def get_random_word(db:Session = Depends(get_db)):
    words = db.query(Word).all()

    if not words:
        raise HTTPException(
            status_code=404,
            detail="No words available in database"
        
        )
    random_word = random.choice(words)
    return random_word

@router.post("/validate-sentence", response_model=ValidateSentenceRequest)
def validate_sentence(request_data: ValidateSentenceRequest):
    word_id = request_data.word_id
    sentence = request_data.sentence
    
    return {"word_id": word_id , "sentence": sentence,}


@router.post("/validate", response_model=ValidateSentenceResponse)
async def validate_sentence_real(req: ValidateSentenceRequest, db: Session = Depends(get_db)):
    db_word = get_word_by_id(db, req.word_id)
    if not db_word:
        raise HTTPException(status_code=404, detail="Word not found")

    result = mock_ai_validation(
        sentence=req.sentence,
        target_word=db_word.word,
        difficulty=db_word.difficulty_level
    )

    return result

@router.post("/practice", response_model=PracticeSubmissionResponse)
def create_practice_submission(submission: PracticeSubmissionCreate, db: Session = Depends(get_db)):
    word = db.query(Word).filter(Word.id == submission.word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    result = mock_ai_validation(
        sentence=submission.submitted_sentence,
        target_word=word.word,
        difficulty='Intermediate'
    )
    
    db_submission = PracticeSubmission(
        user_id=submission.user_id,
        word_id=submission.word_id,
        submitted_sentence=submission.submitted_sentence,
        score=result["score"]
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return PracticeSubmissionResponse(
        id=db_submission.id,
        user_id=db_submission.user_id,
        word_id=db_submission.word_id,
        submitted_sentence=db_submission.submitted_sentence,
        score=db_submission.score,
        suggestion=result["suggestion"],
        timestamp=str(db_submission.timestamp)
    )