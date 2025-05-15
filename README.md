## Get data from sundhed.dk
This script scrapes the Sundhed.dk website to find dentists in a specific municipality.

### For testing
```python
if __name__ == '__main__':
    result = get_dentists(
        municipality_id='751',
        category='Tandlæge'
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
