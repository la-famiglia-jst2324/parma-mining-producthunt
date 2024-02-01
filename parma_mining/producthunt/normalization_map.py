"""Normalization map for producthunt data."""


class ProductHuntNormalizationMap:
    """Normalization map for Product Hunt data."""

    map_json = {
        "Source": "producthunt",
        "Mappings": [
            {
                "SourceField": "name",
                "DataType": "text",
                "MeasurementName": "product name",
            },
            {
                "SourceField": "overall_rating",
                "DataType": "float",
                "MeasurementName": "product overall rating",
            },
            {
                "SourceField": "review_count",
                "DataType": "int",
                "MeasurementName": "product review count",
            },
            {
                "SourceField": "followers",
                "DataType": "int",
                "MeasurementName": "product followers count",
            },
            {
                "SourceField": "reviews",
                "DataType": "nested",
                "MeasurementName": "product reviews",
                "NestedMappings": [
                    {
                        "SourceField": "text",
                        "DataType": "comment",
                        "MeasurementName": "review text",
                    },
                    {
                        "SourceField": "date",
                        "DataType": "date",
                        "MeasurementName": "review date",
                    },
                ],
            },
        ],
    }

    def get_normalization_map(self) -> dict:
        """Return the normalization map."""
        return self.map_json
