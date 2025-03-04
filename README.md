# Kinematics API

Python-based FastAPI for performing inverse and forward kinematics of serial manipulators.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
  - [Add DH Table](#add-dh-table)
  - [Get DH Table](#get-dh-table)
  - [Forward Kinematics](#forward-kinematics)
  - [Get Transformation Matrix](#get-transformation-matrix)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. Install the required packages:
   ```bash
   pip install fastapi uvicorn asyncpg pydantic httpx numpy
   ```

3. Set up your environment variables:
   - `DATABASE_URL`: The connection string for your PostgreSQL database.
   - `API_BASE_URL`: The base URL for the API (e.g., `http://localhost:8000`).

## Usage

To run the API, use the following command:

```bash
uvicorn main:app --reload
```
Replace `main` with the name of your main application file if different.

## Endpoints

### Add DH Table

**POST** `/api/add_dh`

- **Request Body**: A JSON object representing the DH table, including the name and a list of joints.
- **Response**: A message indicating success and the ID of the new DH table.

### Get DH Table

**GET** `/api/get_dh`

- **Query Parameters**:
  - `id`: The ID of the DH table (optional).
  - `name`: The name of the DH table (optional).
- **Response**: The DH table data, including the joints.

### Forward Kinematics

**GET** `/api/fwd_kin`

- **Query Parameters**:
  - `id`: The ID of the stored DH table (optional).
  - `name`: The name of the stored DH table (optional).
  - `joint_values`: A list of joint angles (as repeated query parameters).
- **Response**: The transformation matrix for the end-effector as a nested list.

### Get Transformation Matrix

**GET** `/api/get_transformation_matrix`

- **Query Parameters**:
  - `theta`: The joint angle (in radians).
  - `alpha`: The link twist angle (in radians).
  - `a`: The link length (in meters).
  - `d`: The joint offset (in meters).
- **Response**: The 4x4 transformation matrix as a nested list.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
