from typing import List, Optional
from fastapi import APIRouter, Header, Response
from fastapi.responses import HTMLResponse, PlainTextResponse


router = APIRouter(prefix="/product", tags=["product"])

products = ["watch", "camera", "phone"]


@router.get("/all")
def get_all_products():
    # return products
    data = " ".join(products)
    return Response(content=data, media_type="text/plain")


@router.get("/withheader")
def get_products(response: Response, custom_header: Optional[List[str]] = Header(None)):
    response.headers["custom_response_header"] = " and ".join(custom_header)
    return products


@router.get(
    "/{id}",
    responses={
        200: {
            "content": {
                "text/html": {"example": "<div>Product</div>"},
                "description": "Returns the HTML for an object",
            }
        },
        404: {
            "content": {
                "text/plain": {"example": "Product not available"},
                "description": "A cleartext error message",
            }
        },
    },
)
def get_product(id: int):
    if id > len(products):
        out = "Product not available"
        return PlainTextResponse(content=out, media_type="text/plain")

    product = products[id]
    out = f"""
    <head>
        <style>
        .product {{
            width: 500px;
            height: 30px;
            border: 2px inset green;
            background-color: lightblue;
            text-align: center;
        }}
        </style>
    </head>
    <div class="product">{product}</div>
    """

    return HTMLResponse(content=out, media_type="text/html")
