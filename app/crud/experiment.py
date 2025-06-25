from sqlalchemy.orm import Session
from app.models.experiment import Experiment
from app.schemas.experiment import ExperimentCreate

def create_experiment(db: Session, exp: ExperimentCreate):
    new_exp = Experiment(**exp.dict())
    db.add(new_exp)
    db.commit()
    db.refresh(new_exp)
    return new_exp

def get_experiment_by_id(db: Session, experiment_id: int):
    return db.query(Experiment).filter(Experiment.experiment_id == experiment_id).first()

def get_experiment_by_session_id(db: Session, session_id: str):
    return db.query(Experiment).filter(Experiment.session_id == session_id).first()
