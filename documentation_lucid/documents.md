# Lucid API Documentation

## Search Documents

**POST**  
`https://api.lucid.co/documents/search`

Retrieves information about documents that the authenticated user has at least read-only access to.

By default, documents are sorted by created date from oldest to newest. Providing the `keywords` parameter will cause the documents to be sorted by relevance instead.

> 📘 This endpoint is paginated. For more information, see [Pagination](#).  
> 📘 This endpoint has a per-account rate limit of **300 requests per 5 seconds**.

### Valid Authentication Methods

#### API Key Grants:
- `DocumentRead`

#### OAuth 2.0 User Token Scopes:
- `lucidchart.document.content:readonly`
- `lucidscale.document.content:readonly`
- `lucidspark.document.content:readonly`

### Body Parameters

| Parameter          | Type             | Default Value                | Description |
|-------------------|----------------|------------------------------|-------------|
| `product`        | array of strings | `lucidchart,lucidscale,lucidspark` | Array of Lucid Suite products to filter by. Default value assumes all valid products for the given scopes. |
| `createdStartTime` | date-time        | `0001-01-01T00:00:00Z`       | Date and time to filter documents that have been created after. Default value assumes the beginning of time. |
| `createdEndTime`   | date-time        | `now`                         | Date and time to filter documents that have been created before. Default value assumes the current instant of time. |
| `lastModifiedAfter` | date-time       | `now`                         | Date and time to filter documents that have been modified after. Default value assumes the beginning of time. |
| `keywords`        | string           | _None_                        | Keywords to search against document content and titles. This field is truncated to 400 characters. When provided, results will be sorted by relevance to keyword search. |

### Headers

| Header               | Type   | Required | Default Value | Description |
|----------------------|--------|----------|--------------|-------------|
| `Lucid-Api-Version` | string | ✅ Yes   | `1`          | The API version used in the request. |

### Responses

| Status Code | Description |
|------------|-------------|
| `200 OK`   | Returns an array of Document Resource objects containing information about documents the authenticated user has access to. |
| `400 Bad Request` | Occurs if the request does not contain a body. |
| `403 Forbidden` | Occurs if the `product` query parameter is used and the token’s scopes do not contain the matching readonly scope for each product. |
| `429 Too Many Requests` | Occurs if the account makes more than **300 requests in 5 seconds**. |

---

## Document Contents

**GET**  
`https://api.lucid.co/documents/{id}/contents`

Retrieves information about the contents of the requested **Lucidchart** or **Lucidspark** document.

> 📘 Due to the evolving nature of Lucid documents, an unchanged document may produce varying results over time.  
> 📘 This endpoint has a per-account rate limit of **100 requests per 5 seconds**.  
> 📘 Definitions of content returned can be found at [Document Content resource](#).

### Valid Authentication Methods

#### API Key Grants:
- `DocumentRead`

#### OAuth 2.0 User Token Scopes:
- `lucidchart.document.content:readonly`
- `lucidchart.document.app.picker:readonly`
- `lucidchart.document.app.folder`
- `lucidspark.document.content:readonly`
- `lucidspark.document.app.picker:readonly`
- `lucidspark.document.app.folder`

### Path Parameters

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `id`      | string | ✅ Yes   | ID of the document to retrieve contents from. |

### Headers

| Header               | Type   | Required | Default Value | Description |
|----------------------|--------|----------|--------------|-------------|
| `Lucid-Api-Version` | string | ✅ Yes   | `1`          | The API version used in the request. |

### Responses

| Status Code | Description |
|------------|-------------|
| `200 OK`   | Returns a Document Content resource containing information about the requested document’s content. |
| `403 Forbidden` | Occurs if the app making the request does not have permission to the document, or if the document has been deleted or does not exist. |
| `429 Too Many Requests` | Occurs if the account makes more than **100 requests in 5 seconds**. |

---

## Document Access

For each product, there are three branches of document-related scopes:  

- `{product}.document.content`
- `{product}.document.app.folder`
- `{product}.document.app.picker`

### Scope Descriptions:

1. **document.content**  
   - Grants access to all of the user's documents.

2. **document.app.folder**  
   - Creates a folder dedicated to your app and grants access to all documents and subfolders within it.

3. **document.app.picker**  
   - Initially grants no access to documents.  
   - When your app needs access, you must show the user a **document picker**.  
   - Your app gains access only to the documents **selected by the user**.  
   - Once access is granted, it remains until the user **revokes** it.

---