```python
def main():
    import lucidchart 
    
    # Create shapes
    customer_shape = lucidchart.create_shape('Entity', 'Customer', position=(100, 200))
    order_shape = lucidchart.create_shape('Entity', 'Order', position=(300, 200))
    
    # Create line between Customer and Order
    lucidchart.create_line(customer_shape, order_shape, 'relationship')
    
    # Import to Lucidchart
    lucidchart.import_to_lucidchart([customer_shape, order_shape])

if __name__ == "__main__":
    main()
```