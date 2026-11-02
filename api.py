
import re
from decimal import Decimal

import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator


app = FastAPI(
    title="Real Estate API",
    description="API для обліку будинків, квартир та власників",
    version="1.0.0"
)

DSN = (
    "postgresql://postgres:lab4psm_local_password"
    "@localhost:5432/library"
    "?options=-c%20timezone%3DEurope%2FKyiv"
)


class ApartmentCreate(BaseModel):
    apartment_number: int
    rooms: int = Field(gt=0)
    area: Decimal = Field(gt=0)
    price: Decimal = Field(ge=0)
    building_id: int = Field(gt=0)
    owner_id: int = Field(gt=0)

    @field_validator("apartment_number", mode="before")
    @classmethod
    def validate_apartment_number(cls, value):
        if not re.fullmatch(r"[1-9]\d{0,4}", str(value)):
            raise ValueError("Некоректний номер квартири")
        return int(value)


@app.get("/")
def home():
    return {"message": "Real Estate API працює!"}


@app.get("/apartments")
def get_apartments():
    with psycopg.connect(DSN, row_factory=dict_row) as conn:
        return conn.execute(
            "SELECT * FROM apartments ORDER BY id"
        ).fetchall()


@app.get("/apartments/{apartment_id}")
def get_apartment(apartment_id: int):
    with psycopg.connect(DSN, row_factory=dict_row) as conn:
        apartment = conn.execute(
            "SELECT * FROM apartments WHERE id = %s",
            (apartment_id,)
        ).fetchone()

    if apartment is None:
        raise HTTPException(
            status_code=404,
            detail="Квартиру не знайдено"
        )

    return apartment


@app.post("/apartments", status_code=201)
def create_apartment(apartment: ApartmentCreate):
    with psycopg.connect(DSN, row_factory=dict_row) as conn:
        result = conn.execute(
            """
            INSERT INTO apartments (
                apartment_number, rooms, area, price,
                building_id, owner_id
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *
            """,
            (
                apartment.apartment_number,
                apartment.rooms,
                apartment.area,
                apartment.price,
                apartment.building_id,
                apartment.owner_id
            )
        ).fetchone()

    return result


@app.put("/apartments/{apartment_id}")
def update_apartment(
    apartment_id: int,
    apartment: ApartmentCreate
):
    with psycopg.connect(DSN, row_factory=dict_row) as conn:
        result = conn.execute(
            """
            UPDATE apartments
            SET apartment_number = %s,
                rooms = %s,
                area = %s,
                price = %s,
                building_id = %s,
                owner_id = %s
            WHERE id = %s
            RETURNING *
            """,
            (
                apartment.apartment_number,
                apartment.rooms,
                apartment.area,
                apartment.price,
                apartment.building_id,
                apartment.owner_id,
                apartment_id
            )
        ).fetchone()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Квартиру не знайдено"
        )

    return result


@app.delete("/apartments/{apartment_id}")
def delete_apartment(apartment_id: int):
    with psycopg.connect(DSN) as conn:
        cursor = conn.execute(
            "DELETE FROM apartments WHERE id = %s",
            (apartment_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Квартиру не знайдено"
            )

    return {"message": "Квартиру успішно видалено"}
