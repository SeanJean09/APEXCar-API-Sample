from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(
    title="Apex Car API",
    description="A REST API containing information about 1990s and 2000s cars.",
    version="1.0.0"
)

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
# This will allow a separate HTML/JavaScript frontend
# to communicate with this API later.
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API KEY
API_KEY = "CLASSIC-CARS-2026"


def verify_api_key(x_api_key: str | None):
    """
    Checks whether the client supplied the correct API key.
    """

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key."
        )

# CAR DATABASE
cars = [
    {
        "id": 1,
        "make": "Toyota",
        "model": "Corolla",
        "year": 1998,
        "body_type": "Sedan",
        "engine": "1.6L 4-cylinder",
        "horsepower": 105,
        "transmission": "5-speed manual / 4-speed automatic",
        "drivetrain": "FWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 27-32 MPG",
        "seating_capacity": 5,
        "original_msrp": "$13,000-$16,000",
        "description": "A practical and economical compact sedan known for reliability and inexpensive maintenance.",
        "buyer_notes": "Excellent commuter car. Check for rust, oil leaks, suspension wear, and neglected maintenance.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/4/4f/1996_Toyota_Corolla_sedan%2C_12.28.19.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 2,
        "make": "Honda",
        "model": "Civic",
        "year": 2000,
        "body_type": "Sedan",
        "engine": "1.6L 4-cylinder",
        "horsepower": 106,
        "transmission": "5-speed manual / 4-speed automatic",
        "drivetrain": "FWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 28-35 MPG",
        "seating_capacity": 5,
        "original_msrp": "$13,000-$18,000",
        "description": "A compact car offering good fuel economy, reliability, and a large aftermarket community.",
        "buyer_notes": "Check for transmission issues, rust, oil leaks, and heavily modified examples.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3a/2000_Honda_Civic_Type_R_Championship_White.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 3,
        "make": "Mazda",
        "model": "Miata MX-5",
        "year": 1999,
        "body_type": "Convertible",
        "engine": "1.8L 4-cylinder",
        "horsepower": 140,
        "transmission": "5-speed manual / 4-speed automatic",
        "drivetrain": "RWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 24-29 MPG",
        "seating_capacity": 2,
        "original_msrp": "$19,000-$23,000",
        "description": "A lightweight two-seat roadster celebrated for its handling and driving enjoyment.",
        "buyer_notes": "Rust is a major concern. Inspect the chassis, rocker panels, suspension, and convertible top.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/c/cd/1999_Mazda_MX-5_Miata_front_4.28.18.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 4,
        "make": "Subaru",
        "model": "Impreza WRX",
        "year": 2002,
        "body_type": "Sedan",
        "engine": "2.0L Turbocharged Flat-4",
        "horsepower": 227,
        "transmission": "5-speed manual",
        "drivetrain": "AWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 19-24 MPG",
        "seating_capacity": 5,
        "original_msrp": "$24,000-$26,000",
        "description": "A performance-oriented AWD sedan influenced heavily by Subaru's rally heritage.",
        "buyer_notes": "Many examples have been modified or driven aggressively. Inspect the turbocharger, clutch, drivetrain, and modifications.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/ec/2003_Subaru_Impreza_WRX_Turbo_4.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 5,
        "make": "Mitsubishi",
        "model": "Lancer Evolution VIII",
        "year": 2003,
        "body_type": "Sedan",
        "engine": "2.0L Turbocharged 4-cylinder",
        "horsepower": 271,
        "transmission": "5-speed manual",
        "drivetrain": "AWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 18-23 MPG",
        "seating_capacity": 5,
        "original_msrp": "$29,000-$31,000",
        "description": "A high-performance AWD sedan derived from Mitsubishi's rally program.",
        "buyer_notes": "Expensive examples can have extensive modifications. Inspect turbo, clutch, transmission, differential, and chassis.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/de/2005_Mitsubishi_Lancer_Evolution_VIII_GSR.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 6,
        "make": "Toyota",
        "model": "Supra",
        "year": 1997,
        "body_type": "Coupe",
        "engine": "3.0L Twin-Turbocharged Inline-6",
        "horsepower": 320,
        "transmission": "6-speed manual / 4-speed automatic",
        "drivetrain": "RWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 17-23 MPG",
        "seating_capacity": 4,
        "original_msrp": "$38,000-$40,000",
        "description": "A legendary Japanese sports coupe known for its performance potential and robust engine.",
        "buyer_notes": "Values can be extremely high. Verify originality, accident history, modifications, and engine condition.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/2/2c/Black_1997_Toyota_Supra_Limited_Edition_-_6_Speed_Twin_Turbo_with_Targa_Top.png?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 7,
        "make": "Nissan",
        "model": "Silvia S15",
        "year": 2000,
        "body_type": "Coupe",
        "engine": "2.0L Turbocharged 4-cylinder",
        "horsepower": 247,
        "transmission": "6-speed manual",
        "drivetrain": "RWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 20-26 MPG",
        "seating_capacity": 4,
        "original_msrp": "Varied by market",
        "description": "A lightweight rear-wheel-drive coupe popular among enthusiasts and drifting communities.",
        "buyer_notes": "Check import documentation, chassis condition, modifications, and drivetrain wear.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/b/b1/2000_Nissan_Silvia_Spec_S.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 8,
        "make": "Honda",
        "model": "Integra Type R",
        "year": 1997,
        "body_type": "Coupe",
        "engine": "1.8L Naturally Aspirated 4-cylinder",
        "horsepower": 195,
        "transmission": "5-speed manual",
        "drivetrain": "FWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 25-30 MPG",
        "seating_capacity": 4,
        "original_msrp": "Varied by market",
        "description": "A lightweight performance coupe renowned for its high-revving engine and precise handling.",
        "buyer_notes": "Authenticity matters. Inspect for modifications, accident damage, rust, and engine wear.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Honda_Integra_Type_R_1997.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 9,
        "make": "Ford",
        "model": "Mustang GT",
        "year": 2005,
        "body_type": "Coupe",
        "engine": "4.6L V8",
        "horsepower": 300,
        "transmission": "5-speed manual / 5-speed automatic",
        "drivetrain": "RWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 17-23 MPG",
        "seating_capacity": 4,
        "original_msrp": "$24,000-$26,000",
        "description": "A modernized American muscle car combining traditional V8 performance with a retro-inspired design.",
        "buyer_notes": "Inspect rear axle noise, suspension components, rust, accident history, and engine maintenance.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/08/2005-2009_Ford_Mustang_GT%2C_blue%2C_Golden_Super_Cruise_2026-09-05.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 10,
        "make": "Chevrolet",
        "model": "Corvette C5",
        "year": 2002,
        "body_type": "Coupe",
        "engine": "5.7L V8",
        "horsepower": 350,
        "transmission": "6-speed manual / 4-speed automatic",
        "drivetrain": "RWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 18-27 MPG",
        "seating_capacity": 2,
        "original_msrp": "$40,000-$45,000",
        "description": "A high-performance American sports car using a lightweight chassis and large-displacement V8.",
        "buyer_notes": "Check for electrical problems, suspension wear, clutch condition, and evidence of track use.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/4/4b/2002_Chevrolet_Corvette%2C_Front_Right%2C_10-02-2020.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 11,
        "make": "BMW",
        "model": "M3 E46",
        "year": 2004,
        "body_type": "Coupe",
        "engine": "3.2L Naturally Aspirated Inline-6",
        "horsepower": 333,
        "transmission": "6-speed manual / SMG",
        "drivetrain": "RWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 17-24 MPG",
        "seating_capacity": 4,
        "original_msrp": "$46,000-$50,000",
        "description": "A high-performance German coupe known for its balanced chassis and high-revving engine.",
        "buyer_notes": "Inspect rear subframe, rod bearings, cooling system, VANOS system, and maintenance history.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/30/2004_BMW_M3_2.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 12,
        "make": "Volkswagen",
        "model": "Golf GTI",
        "year": 2006,
        "body_type": "Hatchback",
        "engine": "2.0L Turbocharged 4-cylinder",
        "horsepower": 200,
        "transmission": "6-speed manual / 6-speed DSG",
        "drivetrain": "FWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 24-30 MPG",
        "seating_capacity": 5,
        "original_msrp": "$22,000-$25,000",
        "description": "A practical performance hatchback combining everyday usability with sporty handling.",
        "buyer_notes": "Check timing components, turbocharger, DSG maintenance if equipped, and electrical systems.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/ac/VW_Golf_GTI_V_%28Front_Left%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 13,
        "make": "Acura",
        "model": "RSX Type-S",
        "year": 2006,
        "body_type": "Coupe",
        "engine": "2.0L Naturally Aspirated 4-cylinder",
        "horsepower": 201,
        "transmission": "6-speed manual",
        "drivetrain": "FWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 24-30 MPG",
        "seating_capacity": 4,
        "original_msrp": "$23,000-$25,000",
        "description": "A sporty compact coupe with a high-revving engine and relatively practical interior.",
        "buyer_notes": "Inspect transmission synchros, suspension, oil consumption, rust, and modifications.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/2/21/Acura_RSX_Type_S.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 14,
        "make": "Mazda",
        "model": "RX-8",
        "year": 2005,
        "body_type": "Coupe",
        "engine": "1.3L Renesis Rotary",
        "horsepower": 238,
        "transmission": "6-speed manual / 6-speed automatic",
        "drivetrain": "RWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 16-23 MPG",
        "seating_capacity": 4,
        "original_msrp": "$25,000-$30,000",
        "description": "A unique sports coupe powered by a compact rotary engine and featuring unusual rear-hinged rear doors.",
        "buyer_notes": "Compression testing is extremely important. Rotary engine maintenance and oil consumption require special attention.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/5d/Mazda_RX-8_grey.JPG?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 15,
        "make": "Toyota",
        "model": "MR2 Spyder",
        "year": 2002,
        "body_type": "Convertible",
        "engine": "1.8L 4-cylinder",
        "horsepower": 138,
        "transmission": "5-speed manual / SMT",
        "drivetrain": "RWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 26-32 MPG",
        "seating_capacity": 2,
        "original_msrp": "$23,000-$25,000",
        "description": "A lightweight mid-engine roadster designed around nimble handling rather than outright power.",
        "buyer_notes": "Check for rust, clutch wear, oil consumption, and condition of the soft top.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/2/25/2002_Toyota_MR2_%28ZZW30R%29_Spyder_convertible_%282015-08-07%29_01.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 16,
        "make": "Honda",
        "model": "S2000",
        "year": 2004,
        "body_type": "Convertible",
        "engine": "2.2L Naturally Aspirated 4-cylinder",
        "horsepower": 237,
        "transmission": "6-speed manual",
        "drivetrain": "RWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 20-25 MPG",
        "seating_capacity": 2,
        "original_msrp": "$32,000-$34,000",
        "description": "A high-revving rear-wheel-drive roadster famous for its precise six-speed manual transmission.",
        "buyer_notes": "Inspect differential, clutch, soft top, suspension, accident history, and engine condition.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/68/2007_Honda_S2000.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 17,
        "make": "Nissan",
        "model": "350Z",
        "year": 2005,
        "body_type": "Coupe",
        "engine": "3.5L V6",
        "horsepower": 287,
        "transmission": "6-speed manual / 5-speed automatic",
        "drivetrain": "RWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 19-25 MPG",
        "seating_capacity": 2,
        "original_msrp": "$26,000-$35,000",
        "description": "A relatively affordable rear-wheel-drive sports car powered by Nissan's VQ-series V6.",
        "buyer_notes": "Check oil consumption, clutch, differential, suspension, and evidence of drifting or track use.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/99/Nissan_XXA-Z33_Fairlady_Z_%2823100111194%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 18,
        "make": "Ford",
        "model": "Focus SVT",
        "year": 2003,
        "body_type": "Hatchback",
        "engine": "2.0L Naturally Aspirated 4-cylinder",
        "horsepower": 170,
        "transmission": "6-speed manual",
        "drivetrain": "FWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 24-30 MPG",
        "seating_capacity": 5,
        "original_msrp": "$18,000-$20,000",
        "description": "A compact performance hatchback offering practical dimensions and engaging handling.",
        "buyer_notes": "Inspect suspension components, clutch, electrical systems, and rust.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/a6/2003_Ford_SVT_Focus_ZX3_in_CD_Silver_Metallic%2C_Front_Left%2C_11-05-2022.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 19,
        "make": "Mitsubishi",
        "model": "Eclipse GSX",
        "year": 1999,
        "body_type": "Coupe",
        "engine": "2.0L Turbocharged 4-cylinder",
        "horsepower": 210,
        "transmission": "5-speed manual",
        "drivetrain": "AWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 20-26 MPG",
        "seating_capacity": 4,
        "original_msrp": "$23,000-$25,000",
        "description": "A turbocharged AWD coupe that became popular among performance enthusiasts.",
        "buyer_notes": "Many examples have been modified. Inspect turbo system, transmission, AWD components, and chassis.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/32/1993_Mitsubishi_Eclipse_GSX_%284815542974%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    },

    {
        "id": 20,
        "make": "Lexus",
        "model": "IS 300",
        "year": 2002,
        "body_type": "Sedan",
        "engine": "3.0L Naturally Aspirated Inline-6",
        "horsepower": 215,
        "transmission": "5-speed manual / 5-speed automatic",
        "drivetrain": "RWD",
        "fuel_type": "Gasoline",
        "fuel_economy": "Approximately 19-24 MPG",
        "seating_capacity": 5,
        "original_msrp": "$30,000-$33,000",
        "description": "A compact luxury sport sedan known for its smooth inline-six engine and rear-wheel-drive layout.",
        "buyer_notes": "Check timing belt service, suspension, rust, oil leaks, and transmission condition.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/1/14/LEXUS_IS_300_%28XE20%29_China.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original"
    }
]

# BASIC ROUTES
@app.get("/")
def home():
    return {
        "message": "Welcome to the Classic Car API!",
        "version": "1.0.0",
        "available_endpoints": [
            "/api/cars",
            "/api/cars/random",
            "/api/cars/random/{count}",
            "/api/cars/search",
            "/api/cars/{id}",
            "/api/premium-cars"
        ]
    }


# GET ALL CARS
@app.get("/api/cars")
def get_cars(
    make: str | None = Query(default=None),
    year: int | None = Query(default=None),
    body_type: str | None = Query(default=None)
):
    """
    Returns cars with optional filters.
    """
    results = cars

    if make:
        results = [
            car for car in results
            if car["make"].lower() == make.lower()
        ]

    if year:
        results = [
            car for car in results
            if car["year"] == year
        ]

    if body_type:
        results = [
            car for car in results
            if car["body_type"].lower() == body_type.lower()
        ]

    return {
        "count": len(results),
        "cars": results
    }


# GET ONE CAR
@app.get("/api/cars/{car_id}")
def get_car(car_id: int):
    for car in cars:
        if car["id"] == car_id:
            return car
    raise HTTPException(status_code=404, detail="Car not found.")


# RANDOM CAR
@app.get("/api/cars/random")
def get_random_car():
    return random.choice(cars)


# RANDOM MULTIPLE CARS
@app.get("/api/cars/random/{count}")
def get_random_cars(count: int):
    if count < 1:
        raise HTTPException(status_code=400, detail="Count must be at least 1.")
    if count > len(cars):
        raise HTTPException(status_code=400, detail=f"Maximum number of cars is {len(cars)}.")
    return random.sample(cars, count)


# SEARCH
@app.get("/api/cars/search")
def search_cars(q: str = Query(..., min_length=1)):
    q = q.lower()
    results = []
    for car in cars:
        searchable_text = (
            f"{car['make']} "
            f"{car['model']} "
            f"{car['year']} "
            f"{car['body_type']} "
            f"{car['engine']}"
        ).lower()
        if q in searchable_text:
            results.append(car)
    return {
        "query": q,
        "count": len(results),
        "results": results
    }

# PROTECTED ENDPOINT
@app.get("/api/premium-cars")
def get_premium_cars(
    x_api_key: str | None = Header(default=None)
):

    verify_api_key(x_api_key)

    return {
        "message": "Authenticated successfully.",
        "cars": [
            car for car in cars
            if car["horsepower"] >= 250
        ]
    }
