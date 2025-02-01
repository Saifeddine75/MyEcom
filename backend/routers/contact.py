from fastapi import APIRouter, Depends, status, HTTPException, Response


router = APIRouter(prefix="/contact", tags=['Contact'])