from .audio import router as audio_router
from .users import router as users_router

router = audio_router
router.include_router(users_router)
